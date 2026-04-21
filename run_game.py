"""
run_game.py — Pygame terminal entry point for BattleTest.

Run with:  python run_game.py
The original main.py still works for terminal mode.

IMPORTANT: game modules are imported INSIDE game_main() (deferred), so the
I/O redirects installed by run_in_pygame() are already active when gameplay.py
loads. This is required because gameplay.py calls input() at module scope
(line 57) to ask about online features.
"""

import sys
import os

# When running as a PyInstaller bundle, switch cwd to the bundle directory
# so relative asset paths (audio/, images/, leaderboard.json) resolve correctly.
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

import pygame_terminal


def game_main():
    # Deferred imports — I/O is already redirected by this point
    from gameplay.gameplay import characterBuildIntro, enemyBattle, postCombat, bossBattle

    mainCharacter = characterBuildIntro()
    print("Part 1")
    fightNum = 0
    part = 1

    while mainCharacter.health > 0:
        mainCharacter.fightNum = fightNum

        if fightNum % 5 == 0 and fightNum != 0:
            fightNum = bossBattle(mainCharacter, fightNum, part)
            print('\033[2J\033[3J\033[H', end='')
            part += 1
            print(f"Now we begin part {part}")
        else:
            fightNum = enemyBattle(mainCharacter, fightNum, part)

        postCombat(mainCharacter)
        print('\033[2J\033[3J\033[H', end='')


if __name__ == "__main__":
    pygame_terminal.run_in_pygame(
        game_main,
        title="Stacy's Adventure",
        cols=77,
        rows=35,
        font_size=24,
    )
