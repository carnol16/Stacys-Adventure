import random
import time
from classes.items import StoreItems, CaseItem
from classes.player.createPlayer import Player
from classes.player.armor import Armor
from classes.player.weapon import Weapon
from classes.player.specials import Special
from places.casino.BlackJack import blackjack
from places.casino.horseRacing import race
from audioMixer import SoundManager
import images.openPicture as img


sm = SoundManager()

imagePath = r"images/moon.jpeg"




def openCasino(mainCharacter):
    musicOn = True
    sm.play_music("casino")
    img_window = img.openIMG(imagePath)
    """
    Main casino loop.
    Handles:
    1. Blackjack
    2. Case opening
    3. Leaving the casino
    """
    while True:
        if musicOn == False:
            sm.play_music("casino")
            musicOn = True
            
        print(f"\nYou have {mainCharacter.wallet} monkey money.")
        print("\n--- CASINO MENU ---")
        print("1. Play Blackjack")
        print("2. Open a Case")
        print("3. Horse Racing")
        print("4. Leave Casino")

        casinoChoice = input("What would you like to do? >>> ").strip()

        # Option 1: Play Blackjack
        if casinoChoice == "1":
            if mainCharacter.wallet <= 0:
                print("You're broke! You cannot play Blackjack!")
                continue

            try:
                wager = int(input("How much do you want to bet? >>> "))
            except ValueError:
                print("That's not a valid number.")
                continue

            if wager <= 0:
                print("Bet must be more than zero.")
                continue

            if wager > mainCharacter.wallet:
                print("You don't have that much money!")
                continue

            # Play blackjack
            mainCharacter.wallet, _ = blackjack(mainCharacter.wallet, wager, shoe=None)
            print(f"Your wallet is now: {mainCharacter.wallet}")

            if mainCharacter.wallet <= 0:
                print("You're out of money! Leaving Blackjack...")
                continue

        # Option 2: Open Cases

        elif casinoChoice == "2":

            # Get indices of all CaseItems in inventory  
           # OPTION 2: Open Cases
            case_indices = [i for i, item in enumerate(mainCharacter.items) if isinstance(item, CaseItem)]

            if not case_indices:
                print("You have no cases to open!")
                continue

            print("\nYour cases:")
            for i, idx in enumerate(case_indices):
                print(f"{i} - {mainCharacter.items[idx].name}")

            try:
                chosen_index = int(input("Which case would you like to open? >>> "))
            except ValueError:
                print("Invalid choice.")
                continue

            if not (0 <= chosen_index < len(case_indices)):
                print("That's not a valid case number.")
                continue

            actual_index = case_indices[chosen_index]
            case = mainCharacter.items[actual_index]
            sm.play_sfx("caseOpen")
            # Spinner animation
            print(f"\nOpening {case.name}", end="")

            for _ in range(17):
                print(".", end="", flush=True)
                time.sleep(0.5)
            print()
            
            
            del mainCharacter.items[actual_index]
            # Open the case, apply reward automatically
            reward = case.openCase(mainCharacter)

            # Remove the case

        # Option 3: Horse Racing
        elif casinoChoice == "3":
            if mainCharacter.wallet <= 0:
                print("You're broke! You cannot race horses!")
                continue

            try:
                wager = int(input("How much do you want to bet? >>> "))
            except ValueError:
                print("That's not a valid number.")
                continue

            if wager <= 0:
                print("Bet must be more than zero.")
                continue

            if wager > mainCharacter.wallet:
                print("You don't have that much money!")
                continue

            # Play horse racing
            sm.fadeout_music(1000)
            time.sleep(1)
            musicOn = False
            mainCharacter.wallet = race(mainCharacter.wallet, wager)
            print(f"Your wallet is now: {mainCharacter.wallet}")

            if mainCharacter.wallet <= 0:
                print("You're out of money! Leaving Horse Racing...")
                continue

        # Option 4: Leave Casino
        elif casinoChoice == "4":
            print("Leaving the casino...")
            sm.fadeout_music(1000)
            # Destroy the image window automatically
            img.openIMG(destroy=True)
            return

        # Invalid input
        else:
            print("Invalid choice. Pick 1, 2, 3, or 4.")

