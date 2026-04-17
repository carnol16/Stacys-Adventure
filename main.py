from gameplay.gameplay import characterBuildIntro, enemyBattle, postCombat, bossBattle
from classes.player.createPlayer import Player, NPC
import os
from audioMixer import SoundManager
import json
import datetime
import atexit
import pygame

atexit.register(pygame.quit)



mainCharacter = Player("boat man", "blue", "mommy" )
#mainCharacter.activeParty = (NPC("Parim the Iguana", "blue"))

mainCharacter = characterBuildIntro()      
print("Part 1")                                                                                                      
fightNum = 0
part = 1
# GAMEPLAY LOOP
while mainCharacter.health > 0:
    
    mainCharacter.fightNum = fightNum

    if fightNum % 5 == 0 and fightNum != 0:
        fightNum = bossBattle(mainCharacter, fightNum, part)
        print('\033[2J\033[3J\033[H', end='')  # Clear screen and scrollback
        part += 1
        print(f"Now we begin part {part} ")
        
    else:
        fightNum = enemyBattle(mainCharacter, fightNum, part)
        #print('\033[2J\033[3J\033[H', end='')  # Clear screen and scrollback
    
    postCombat(mainCharacter)
    print('\033[2J\033[3J\033[H', end='') 
