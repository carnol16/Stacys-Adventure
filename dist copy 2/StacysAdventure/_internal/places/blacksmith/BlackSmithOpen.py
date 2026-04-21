from classes.items import StoreItems
from .Build import craftableItems, build
from PIL import Image
import time
from audioMixer import SoundManager
import images.openPicture as img

sm = SoundManager()

imagePath = r"images/blacksmith.jpg" 




def openBlacksmith(mainCharacter):
    sm.play_music("blacksmith")
    img_window = img.openIMG(imagePath)

    while True:
        print(f"\nYou have {mainCharacter.wallet} monkey money.")
        print("\n--- BLACKSMITH MENU ---")
        print("1. BUILD")
        print("2. REPAIR")
        print("3. SCAVENGE")
        print("4. Leave")

        blacksmithChoice = input("What would you like to do? >>> ").strip()
        # BUILD OPTION

        if blacksmithChoice == "1":
            
            print("\n--- CRAFTABLE ITEMS ---")
            for i, item in enumerate(craftableItems):
                mats = ", ".join([f"{k}: {v}" for k, v in item.required_items.items()])
                print(f"{i}. {item.name}  |  requires: {mats}")

            choice = input("\nWhich item would you like to craft? >>> ").strip()

            if not choice.isdigit() or int(choice) not in range(len(craftableItems)):
                print("Invalid choice!")
                continue

            chosen = craftableItems[int(choice)]
            build(mainCharacter, chosen)
            continue

        # REPAIR
        elif blacksmithChoice == "2":
            if not mainCharacter.armor:
                print("You have no armor equipped.")
                continue

            arm = mainCharacter.armor
            print(f"\nArmor: {arm.name}")
            print(f"Durability: {arm.durability}")

            if arm.durability == 100:
                print("Your armor does not need repairs.")
                continue

            cost = arm.repairCost()
            print(f"Repair cost: {cost} coins")

            confirm = input("Repair armor? (yes/no): ").lower()
            if confirm != "yes":
                continue

            if mainCharacter.wallet < cost:
                print("Not enough coins!")
                continue

            mainCharacter.wallet -= cost
            arm.repair()

            print(f"{arm.name} has been fully repaired!")
            continue


        # SCAVENGE 

        elif blacksmithChoice == "3":
            print("You scavenge for scraps...")
            continue


        # EXIT
        elif blacksmithChoice == "4":
            print("You leave the blacksmith.")
            sm.fadeout_music(1000)        
            img.openIMG(destroy=True)
 
            break

        else:
            print("Invalid option, try again!")
