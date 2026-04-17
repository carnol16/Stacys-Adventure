import pygame
import os

musicVol = 0.5
sfxVol = 0.3
class SoundManager:
    def __init__(self, base_folder="audio", sound_enabled=True):
        pygame.mixer.init()

        
        self.sound_enabled = sound_enabled
        self.base_folder = base_folder

        self.sfx = {}
        self.music = {}
        self.battle = {}

        
        self.load_audio()

    # AUTO-SCANNER
    def load_audio(self):
        """
        Automatically scans all subfolders.
        Rule:
          - files inside /places/ = music
          - files in root audio/ = sound effects
        """
        for root, dirs, files in os.walk(self.base_folder):
            for file in files:
                if not file.lower().endswith((".ogg", ".wav", ".mp3")):
                    continue

                full_path = os.path.join(root, file)
                key = os.path.splitext(file)[0]  # name without extension

                # Decide category
                rel = os.path.relpath(root, self.base_folder)

                if rel.startswith("music"):
                    # Treat everything in /places/ as MUSIC
                    self.music[key] = full_path
                elif rel.startswith("sfx"):
                    # Everything else is SFX
                    self.sfx[key] = pygame.mixer.Sound(full_path)
                elif rel.startswith("battle"):
                    self.music[key] = full_path



    # SOUND EFFECTS
    def play_sfx(self, name):
        if not self.sound_enabled:
            #print(f"(disabled) would play SFX: {name}")
            return

        if name in self.sfx:
            self.sfx[name].play()
            
            
        else:
            print(f"[ERROR] SFX '{name}' not found")

    # MUSIC
    def play_music(self, name, loops=-1, fade_ms=500):
        if name not in self.music:
            #print(f"[ERROR] Music '{name}' not found")
            return
        if not self.sound_enabled:
            #print(f"(disabled) would play Music: {name}")
            return
        pygame.mixer.music.set_volume(musicVol)
        pygame.mixer.music.load(self.music[name])
        pygame.mixer.music.play(loops, fade_ms=fade_ms)

    def stop_music(self):
        pygame.mixer.music.stop()
    
    def fadeout_music(self, ms=500):
        pygame.mixer.music.fadeout(ms)

    # DEBUG PRINT
    def print_loaded(self):
        print("\n=== SOUND EFFECTS ===")
        for key in self.sfx:
            print(f"  {key} → sm.play_sfx('{key}')")

        print("\n=== MUSIC ===")
        for key in self.music:
            print(f"  {key} → sm.play_music('{key}')")

        print("\n======================\n")




'''sm = SoundManager()

sm.print_loaded()'''

# Shared singleton — import this instead of creating new SoundManager() instances
_shared_sm = None

def get_sound_manager():
    global _shared_sm
    if _shared_sm is None:
        _shared_sm = SoundManager()
    return _shared_sm