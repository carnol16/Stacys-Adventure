"""
pygame_terminal.py — Pygame-based terminal emulator for BattleTest.

Redirects sys.stdout and builtins.input to a pygame window so the game runs
without needing a real terminal. Game logic runs in a background thread;
the main thread handles the pygame event loop and rendering.
"""

import sys
import os
import re
import queue
import threading
import builtins
import pygame

# ── ANSI color maps ────────────────────────────────────────────────────────────

DEFAULT_FG    = (204, 204, 204)
DEFAULT_BG    = (0, 0, 0)
WINDOW_BG     = (12, 12, 12)
IMAGE_PANEL_W = 350          # width of the right-side image panel in pixels
IMAGE_PANEL_BG = (20, 20, 20)

ANSI_FG = {
    30: (0, 0, 0),        31: (205, 49,  49),   32: (13,  188, 121),
    33: (229, 229, 16),   34: (36,  114, 200),  35: (188, 63,  188),
    36: (17,  168, 205),  37: (229, 229, 229),
    90: (102, 102, 102),  91: (241, 76,  76),   92: (35,  209, 139),
    93: (245, 245, 67),   94: (59,  142, 234),  95: (214, 112, 214),
    96: (41,  184, 219),  97: (255, 255, 255),
}

ANSI_BG = {
    40:  (0,   0,   0),   41:  (205, 49,  49),  42:  (13,  188, 121),
    43:  (229, 229, 16),  44:  (36,  114, 200), 45:  (188, 63,  188),
    46:  (17,  168, 205), 47:  (229, 229, 229),
    100: (102, 102, 102), 101: (241, 76,  76),  102: (35,  209, 139),
    103: (245, 245, 67),  104: (59,  142, 234), 105: (214, 112, 214),
    106: (41,  184, 219), 107: (255, 255, 255),
}


# ── ANSI parser ────────────────────────────────────────────────────────────────

class ANSIParser:
    """
    Streaming ANSI escape sequence parser.
    Call feed(text) → list of (char, fg, bg) tuples.
    Screen-clear sequences yield ('CLEAR', None, None).
    Maintains current color state between calls.
    """

    def __init__(self):
        self.fg = DEFAULT_FG
        self.bg = DEFAULT_BG
        self._esc_buf = ''
        self._in_esc  = False

    def feed(self, text):
        out = []
        for ch in text:
            if self._in_esc:
                self._esc_buf += ch
                if ch.isalpha():                 # end of escape sequence
                    out.extend(self._flush_esc())
                    self._in_esc  = False
                    self._esc_buf = ''
            elif ch == '\033':
                self._in_esc  = True
                self._esc_buf = '\033'
            else:
                out.append((ch, self.fg, self.bg))
        return out

    def _flush_esc(self):
        m = re.match(r'\033\[([0-9;]*)([A-Za-z])', self._esc_buf)
        if not m:
            return []
        params_str, cmd = m.group(1), m.group(2)
        params = ([int(p) if p else 0 for p in params_str.split(';')]
                  if params_str else [0])

        if cmd == 'm':
            self._apply_sgr(params)
        elif cmd == 'J':
            # Erase in Display (2J = clear screen, 3J = clear scrollback)
            return [('CLEAR', None, None)]
        # H (cursor home), A/B/C/D (cursor movement), etc. — ignored
        return []

    def _apply_sgr(self, params):
        for p in params:
            if p == 0:
                self.fg, self.bg = DEFAULT_FG, DEFAULT_BG
            elif 30 <= p <= 37 or 90 <= p <= 97:
                self.fg = ANSI_FG.get(p, DEFAULT_FG)
            elif p == 39:
                self.fg = DEFAULT_FG
            elif 40 <= p <= 47 or 100 <= p <= 107:
                self.bg = ANSI_BG.get(p, DEFAULT_BG)
            elif p == 49:
                self.bg = DEFAULT_BG


# ── Terminal buffer ────────────────────────────────────────────────────────────

class TerminalBuffer:
    """
    Thread-safe text buffer representing terminal screen content.
    Each line is a list of (char, fg_color, bg_color) tuples.
    """

    def __init__(self, cols=160, rows=40, scrollback=2000):
        self.cols      = cols
        self.rows      = rows
        self.scrollback = scrollback
        self.lines     = [[]]           # list of lines
        self.lock      = threading.Lock()
        self.dirty     = True
        self.input_mode   = False       # True while waiting for user input
        self.scroll_offset = 0          # lines scrolled up from bottom
        self.image_path  = None         # absolute path of image to show (or None)
        self.image_dirty = False        # signals main thread to reload image

    # ── writes (called from game thread) ──────────────────────────────────────

    def write_events(self, events):
        """Consume a list of (char, fg, bg) events from ANSIParser."""
        with self.lock:
            for char, fg, bg in events:
                if char == 'CLEAR':
                    self.lines = [[]]
                    self.scroll_offset = 0
                elif char == '\n':
                    self.lines.append([])
                    if len(self.lines) > self.scrollback:
                        self.lines = self.lines[-self.scrollback:]
                elif char == '\r':
                    pass   # ignore bare carriage return
                else:
                    self.lines[-1].append((char, fg, bg))
            self.dirty = True

    # ── writes (called from main/UI thread for typed characters) ──────────────

    def write_char(self, char, fg=DEFAULT_FG, bg=DEFAULT_BG):
        """Write a single character directly (typed input from main thread)."""
        with self.lock:
            if char == '\n':
                self.lines.append([])
                if len(self.lines) > self.scrollback:
                    self.lines = self.lines[-self.scrollback:]
            elif char != '\r':
                self.lines[-1].append((char, fg, bg))
            self.dirty = True

    def backspace(self):
        """Remove the last character of the current line (backspace key)."""
        with self.lock:
            if self.lines[-1]:
                self.lines[-1].pop()
                self.dirty = True

    # ── scroll / view ─────────────────────────────────────────────────────────

    def scroll(self, delta):
        with self.lock:
            max_scroll = max(0, len(self.lines) - self.rows)
            self.scroll_offset = max(0, min(self.scroll_offset + delta, max_scroll))
            self.dirty = True

    def scroll_to_bottom(self):
        with self.lock:
            self.scroll_offset = 0
            self.dirty = True

    def get_visible_lines(self):
        """Return a snapshot of the currently visible lines for rendering."""
        with self.lock:
            total = len(self.lines)
            if self.scroll_offset > 0:
                end   = min(total, total - self.scroll_offset + self.rows)
                end   = max(self.rows, total - self.scroll_offset)
                end   = min(end, total)
                start = max(0, end - self.rows)
            else:
                start = max(0, total - self.rows)
                end   = total
            return [list(line) for line in self.lines[start:end]]

    def cursor_col(self):
        """Column position of the cursor (length of the last line)."""
        with self.lock:
            return len(self.lines[-1])

    def is_at_bottom(self):
        with self.lock:
            return self.scroll_offset == 0


# ── stdout redirect ────────────────────────────────────────────────────────────

class StdoutRedirect:
    """File-like object that replaces sys.stdout/sys.stderr."""

    def __init__(self, buf, parser):
        self.buf    = buf
        self.parser = parser
        self.encoding = 'utf-8'
        self.errors   = 'replace'

    def write(self, text):
        if text:
            events = self.parser.feed(str(text))
            self.buf.write_events(events)
        return len(text) if text else 0

    def flush(self):
        pass   # rendering happens on pygame tick

    def fileno(self):
        raise OSError("Not a real file descriptor")

    def isatty(self):
        return True  # ensures colorama emits raw ANSI on all platforms


# ── input capture ──────────────────────────────────────────────────────────────

class InputCapture:
    """
    Replacement for builtins.input().
    Writes the prompt to the terminal buffer, then blocks the game thread on a
    Queue until the main thread delivers a completed input line (on Enter).
    """

    def __init__(self, buf, parser, input_queue):
        self.buf         = buf
        self.parser      = parser
        self.input_queue = input_queue

    def __call__(self, prompt=''):
        if prompt:
            events = self.parser.feed(str(prompt))
            self.buf.write_events(events)
        self.buf.scroll_to_bottom()
        self.buf.input_mode = True
        result = self.input_queue.get()   # blocks game thread
        self.buf.input_mode = False
        return result


# ── image helpers ─────────────────────────────────────────────────────────────

def _load_image_surface(path, panel_w, panel_h):
    """Load an image file and scale it to fit inside the panel, centred."""
    try:
        surf = pygame.image.load(path).convert()
        img_w, img_h = surf.get_size()
        scale = min(panel_w / img_w, panel_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        return pygame.transform.smoothscale(surf, (new_w, new_h))
    except Exception:
        return None


def _render_image_panel(screen, image_surf, panel_x, win_h):
    """Draw the right-side image panel (dark background + centred image)."""
    panel_rect = pygame.Rect(panel_x, 0, IMAGE_PANEL_W, win_h)
    pygame.draw.rect(screen, IMAGE_PANEL_BG, panel_rect)
    # 1-px separator line
    pygame.draw.line(screen, (60, 60, 60), (panel_x, 0), (panel_x, win_h))
    if image_surf:
        iw, ih = image_surf.get_size()
        ix = panel_x + (IMAGE_PANEL_W - iw) // 2
        iy = (win_h - ih) // 2
        screen.blit(image_surf, (ix, iy))


# ── rendering ──────────────────────────────────────────────────────────────────

def _get_font(size=12):
    candidates = ('Courier New', 'Courier', 'Consolas', 'Lucida Console',
                  'Monospace', 'DejaVu Sans Mono')
    for name in candidates:
        f = pygame.font.SysFont(name, size)
        if f:
            return f
    return pygame.font.Font(None, size)


def _draw_span(screen, font, text, x, y, char_w, char_h, fg, bg):
    if not text:
        return
    w = len(text) * char_w
    if bg not in (DEFAULT_BG, WINDOW_BG):
        pygame.draw.rect(screen, bg, (x, y, w, char_h))
    # antialias=False gives sharper text at small sizes
    surf = font.render(text, True, fg)
    screen.blit(surf, (x, y))


def _render_terminal(screen, font, buf, char_w, char_h, cursor_tick):
    screen.fill(WINDOW_BG)
    visible = buf.get_visible_lines()

    for row_i, line in enumerate(visible):
        if not line:
            continue
        x = 0
        y = row_i * char_h

        # Batch consecutive same-colored characters into spans
        span_chars = [line[0][0]]
        span_fg    = line[0][1]
        span_bg    = line[0][2]

        for char, fg, bg in line[1:]:
            if fg == span_fg and bg == span_bg:
                span_chars.append(char)
            else:
                _draw_span(screen, font, ''.join(span_chars),
                           x, y, char_w, char_h, span_fg, span_bg)
                x += len(span_chars) * char_w
                span_chars = [char]
                span_fg, span_bg = fg, bg

        _draw_span(screen, font, ''.join(span_chars),
                   x, y, char_w, char_h, span_fg, span_bg)

    # Draw blinking cursor when waiting for input
    if buf.input_mode and buf.is_at_bottom():
        last_row = len(visible) - 1
        if last_row < 0:
            last_row = 0
        col = buf.cursor_col()
        cx  = col * char_w
        cy  = last_row * char_h
        if cursor_tick < 30:
            pygame.draw.rect(screen, DEFAULT_FG, (cx, cy, char_w, char_h))
        else:
            pygame.draw.rect(screen, DEFAULT_FG, (cx, cy, char_w, char_h), 1)


# ── game thread wrapper ────────────────────────────────────────────────────────

def _run_game_safe(game_func, buf, parser):
    try:
        game_func()
    except SystemExit:
        buf.input_mode = False
        buf.write_events(parser.feed(
            '\n\n[Game over — close the window to exit]\n'
        ))
    except Exception as e:
        import traceback
        buf.input_mode = False
        tb = traceback.format_exc()
        buf.write_events(parser.feed(f'\n\nFATAL ERROR: {e}\n{tb}\n'))


# ── main launcher ──────────────────────────────────────────────────────────────

def run_in_pygame(game_func, title="BattleTest", cols=160, rows=40, font_size=12):
    """
    Launch game_func inside a pygame terminal emulator window.

    game_func() is called in a background thread AFTER sys.stdout and
    builtins.input are redirected, so any imports inside game_func also
    see the redirected I/O.
    """
    pygame.init()

    font   = _get_font(font_size)
    char_w = font.size('M')[0]
    char_h = font.get_linesize()

    term_w = cols * char_w
    win_w  = term_w + IMAGE_PANEL_W
    win_h  = rows * char_h

    screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
    pygame.display.set_caption(title)

    buf         = TerminalBuffer(cols=cols, rows=rows)
    parser      = ANSIParser()
    input_queue = queue.Queue()

    stdout_redirect = StdoutRedirect(buf, parser)
    input_capture   = InputCapture(buf, parser, input_queue)

    # ── install redirects ──────────────────────────────────────────────────────
    orig_stdout    = sys.stdout
    orig_stderr    = sys.stderr
    orig_input     = builtins.input
    orig_os_system = os.system

    sys.stdout    = stdout_redirect
    sys.stderr    = stdout_redirect
    builtins.input = input_capture

    def patched_os_system(cmd):
        if cmd.strip() in ('clear', 'cls'):
            buf.write_events([('CLEAR', None, None)])
        else:
            orig_os_system(cmd)

    os.system = patched_os_system

    # ── patch image module to render into the pygame panel ────────────────────
    import images.openPicture as _img_module

    def _patched_openIMG(imagePath=None, destroy=False):
        with buf.lock:
            if destroy or imagePath is None:
                buf.image_path  = None
            else:
                buf.image_path  = os.path.abspath(imagePath)
            buf.image_dirty = True
            buf.dirty       = True

    _img_module.openIMG = _patched_openIMG

    # ── start game thread ──────────────────────────────────────────────────────
    game_thread = threading.Thread(
        target=_run_game_safe,
        args=(game_func, buf, parser),
        daemon=True,
    )
    game_thread.start()

    # ── pygame event loop ──────────────────────────────────────────────────────
    current_input     = []    # characters currently being typed
    cursor_tick       = 0
    current_image_surf = None  # scaled pygame Surface or None
    clock             = pygame.time.Clock()
    running           = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if buf.input_mode:
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            line = ''.join(current_input)
                            buf.write_char('\n')
                            input_queue.put(line)
                            current_input.clear()
                            cursor_tick = 0
                            buf.scroll_to_bottom()

                        elif event.key == pygame.K_BACKSPACE:
                            if current_input:
                                current_input.pop()
                                buf.backspace()

                        else:
                            ch = event.unicode
                            if ch and ch.isprintable():
                                current_input.append(ch)
                                buf.write_char(ch)

                elif event.type == pygame.MOUSEWHEEL:
                    # Scroll up = positive event.y → increase scroll_offset
                    buf.scroll(-event.y * 3)

                elif event.type == pygame.VIDEORESIZE:
                    new_cols = max(80, (event.w - IMAGE_PANEL_W) // char_w)
                    new_rows = max(24, event.h // char_h)
                    buf.cols = new_cols
                    buf.rows = new_rows
                    screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )

            # Reload image if game thread changed it
            if buf.image_dirty:
                with buf.lock:
                    path = buf.image_path
                    buf.image_dirty = False
                if path:
                    current_image_surf = _load_image_surface(path, IMAGE_PANEL_W, win_h)
                else:
                    current_image_surf = None
                buf.dirty = True

            # Re-render whenever buffer changed or cursor needs blinking
            if buf.dirty:
                term_panel_w = screen.get_width() - IMAGE_PANEL_W
                _render_terminal(screen, font, buf, char_w, char_h, cursor_tick)
                _render_image_panel(screen, current_image_surf,
                                    term_panel_w, screen.get_height())
                pygame.display.flip()
                buf.dirty = False

            cursor_tick = (cursor_tick + 1) % 60
            if buf.input_mode:
                buf.dirty = True   # keep redrawing for cursor blink

            clock.tick(60)

    except KeyboardInterrupt:
        pass

    # ── cleanup ────────────────────────────────────────────────────────────────
    sys.stdout     = orig_stdout
    sys.stderr     = orig_stderr
    builtins.input = orig_input
    os.system      = orig_os_system
    pygame.quit()
