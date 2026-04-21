import random
from classes.items import StoreItems
from classes.player.createPlayer import Player
from classes.player.armor import Armor
from classes.player.specials import Special
from classes.priceGrab import csPriceChecker
from classes.priceGrab import marketItem
from classes.items import CaseItem
from PIL import Image
import time
from audioMixer import SoundManager
import images.openPicture as img

sm = SoundManager()


imagePath = r"images/bigTop.jpg"

music = ["shop1", "shop2", "shop3"]



def openStore(mainCharacter):
    img_window = img.openIMG(imagePath)
    pickedMusic = random.choice(music)
    
    sm.play_music(pickedMusic)
    print(f"\nWELCOME TO BIG TOP {mainCharacter.name}!")

    caseChoices = [
        "Chroma Case",
        # "Gamma Case",
        # "Dreams & Nightmares Case",
        # "Kilowatt Case",
        "Fever Case"
        # "CS:GO Weapon Case"
    ]

    #pickedCase = caseChoices[random.randint(0,4)]

    pickedCase = caseChoices[random.randint(0,1)]

    casePrice = random.randint(10,50)  # default price
    caseName = pickedCase

    itemChoices = [
        StoreItems("Daddy's Belt", 100, True, False, True, False, False, 100, 10, 60, True),
        StoreItems("Cased Hardened AK-47", 423, True, False, True, False, False, 35, 15, 15, True),
        StoreItems("Gamer Girl Bath Water", 30, False, True, False, True, False, 45, 75, 0),
        StoreItems("Sam Keh's Secret Love For Brian", 10, True, False, False, True, False, 200, 5, 1),
        StoreItems("Top Ramen", 1, False, True, False, True, False, 5, 100, 0),
        StoreItems("Pink Suit", 70, False, False, False, False, True, 43, 45, 0, False),
        StoreItems(caseName, casePrice, False, True, False, False, False, 0, 60, 0),
    ]

    availableItems = []

    while len(availableItems) < 2:
        chosenItem = random.choices(
            itemChoices, weights=[item.rarity for item in itemChoices], k=1
        )[0]
        availableItems.append(chosenItem)

    """
        while len(availableItems) < 2:
        chosenItem = random.choices(
            itemChoices, weights=[item.rarity for item in itemChoices], k=1
        )[0]
        availableItems.append(chosenItem)
        #print(chosenItem.name, chosenItem.price)
        print("Items For Sale:")
    """

    # STORE MENU LOOP
    while True:   
        print(f"\nCurrent balance: {mainCharacter.wallet}")
        print("\nStore Menu:")
        print("1. Purchase")
        print("2. Sell")
        print("3. Leave")

        try:
            choice = int(input("Choose an action (1-3): ").strip())
        except ValueError:
            print("YOU GONNA BREAK IT")
            continue

        if choice == 1:
            freeSpace = mainCharacter.space - len(mainCharacter.items)
            print("\n\nItems For Sale:")
            for i, item in enumerate(availableItems):
                itemType = ""
                if item.items == True  and item.damage == True :
                    itemType = "DMG to Enemy"
                elif item.items == True and item.heal == True:
                    itemType = "Heal to Player"
                elif item.armor == True:
                    itemType = "DEF for Player"
                elif item.weapon == True:
                    itemType = "DMG for Player"
                print(f"{i+1}. {item.name}: Price: ${item.price}: +{item.amount} {itemType}")
            if freeSpace > 0:
                pickedItem = int(input("\nitem 1 or 2? \nPress 3 to purchase neither: ").strip())
                if pickedItem in [1, 2]:
                    chosen = availableItems[pickedItem - 1]

                    if mainCharacter.wallet >= chosen.price:
                        mainCharacter.wallet -= chosen.price
                        print(
                            f"You bought {chosen.name} for {chosen.price} Monkey Money!"
                        )

                        if "Case" in chosen.name:
                            mainCharacter.items.append(CaseItem(chosen.name))
                            print(f"{chosen.name} added to your inventory!")

                        elif chosen.armor:
                            print(f"{chosen.name} is armor!")

                            equip = input("Equip it now? (yes/no): ").lower()

                            if equip == "yes":
                                from classes.player.armor import Armor

                                newArmor = Armor(chosen.name, chosen.amount)

                                # Remove old armor if exists
                                if mainCharacter.armor:
                                    try:
                                        mainCharacter.armor.detach(mainCharacter)
                                    except:
                                        pass

                                newArmor.attach(mainCharacter)
                                continue  # Skip storing the item
                        elif chosen.weapon:
                            print(f"{chosen.name} is weapon!")

                            equip = input("Equip it now? (yes/no): ").lower()

                            if equip == "yes":
                                from classes.player.weapon import Weapon

                                newWeapon = Weapon(chosen.name, chosen.amount)

                                # Remove old armor if exists
                                if mainCharacter.weapon:
                                    try:
                                        mainCharacter.weapon.detach(mainCharacter)
                                    except:
                                        pass

                                newWeapon.attach(mainCharacter)
                                continue  # Skip storing the item
                            
                        elif chosen.specials == False:
                            mainCharacter.items.append(
                                StoreItems(chosen.name, chosen.price, False, True, chosen.damage, chosen.heal, chosen.armor, chosen.amount, chosen.rarity, chosen.manaCost)
                            )
                        else:
                            mainCharacter.attacks.append(
                                Special(chosen.name, 0, chosen.damage, chosen.heal, chosen.amount, chosen.manaCost)) 
                    else:
                        print("Not enough Monkey Money!")
                elif pickedItem == 3:
                    continue
                else:
                    print("Invalid choice")

            else:
                print("sorry baddie, no space")
                dropItem = input("would you like to dispose of something??? ")
                if dropItem == "yes":
                    print("Here are the items you have currently:")
                    counter = 0
                    for i in mainCharacter.items:
                        print(counter, i.name)
                        counter += 1

                    removeIndex = int(input("Which number to remove? "))
                    if 0 <= removeIndex < len(mainCharacter.items):
                        removed = mainCharacter.items.pop(removeIndex)
                        print(f"Removed {removed.name}.")
                    else:
                        print("Invalid index.")

        elif choice == 2:
            if not mainCharacter.items:
                print("\nYou have nothing to sell!")
                continue

            print("\n===== SELL ITEMS =====")
            for i, item in enumerate(mainCharacter.items):
                print(f"{i}: {item.name}")

            try:
                idx = int(input("\nEnter index of item to sell: ").strip())
                if idx < 0 or idx >= len(mainCharacter.items):
                    print("Invalid index.")
                    continue

                itemToSell = mainCharacter.items[idx]

                # CASES SELL AT MARKET VALUE
                if "Case" in itemToSell.name:
                    market = csPriceChecker()
                    caseInfo = market.getItem(itemToSell.name)

                    if caseInfo.price is not None:
                        sellPrice = int(caseInfo.price * 10)  # same multiplier used when buying
                    else:
                        sellPrice = 10  # fallback if API fails

                    print(f"\nMarket price detected for {itemToSell.name}: {sellPrice}")

                else:
                    # Regular items sell for 50% price
                    if hasattr(itemToSell, "price"):
                        sellPrice = int(itemToSell.price * 0.5)
                    else:
                        sellPrice = 5

                confirm = input(f"Sell {itemToSell.name} for {sellPrice}? (yes/no): ").lower()
                if confirm != "yes":
                    print("Sell canceled.")
                    continue

                del mainCharacter.items[idx]
                mainCharacter.wallet += sellPrice

                print(f"Sold {itemToSell.name} for {sellPrice} coins!")

            except ValueError:
                print("Invalid input.")

         

        elif choice == 3:
            print("Thanks for stopping by!!!")
            sm.fadeout_music(1000)
            img.openIMG(destroy=True)

            return

        else:
            print("Invalid choice")
