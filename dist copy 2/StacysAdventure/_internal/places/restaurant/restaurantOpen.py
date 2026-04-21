from classes.player.createPlayer import Player
from audioMixer import SoundManager as sm
from classes.items import StoreItems
import images.openPicture as img


import random

foodItem = [
    ["Pourage", 3, 5],
    ["Momma's Famous Mash Potatoes", 5, 15],
    ["CHICKEN BOX", 10, 25]
    ]


def openResturant(mainCharacter):
    #sm.play_music(None)
    #img_window = img.openIMG(None)
    
    pickedFood = random.choice(foodItem)
    
    """
    1. Get Mana
    2. Leave
    5413. Clean Dirty Dishes
    """





    print("Welcome to Krispy Krunchy Chicken")
    while True:
        print(f"\nYou have {mainCharacter.wallet} monkey money.")
        
        print("\n--- FOOD MENU ---")
       #print("1. HP Rich Food")
        print("1. Mana Rich Food")
        print("2. Leave")
        if any(a.name == "Dirty Dishes" for a in mainCharacter.attacks):
            print("5413. Clean Dirty Dishes")
        

        
        try:
            foodChoice = input("Choose an action (1-2): ").strip()
        except ValueError:
            print("YOU GONNA BREAK IT")
            continue
        
        
        if foodChoice == "1":
            if mainCharacter.wallet <= 0:
                print("This ain't no food pantry")
                continue
            else:
                print(f"Today's special is {pickedFood[0]} and gives {pickedFood[2]} mana")
                choice = input(f"Would you like it for {pickedFood[1]}? (y/n): ")
                if choice == "y":
                    if mainCharacter.wallet >= pickedFood[1]:
                        
                        mainCharacter.mana += pickedFood[2]
                        print(f"You Consumed {pickedFood[0]}!!!\nNew Mana Total: {mainCharacter.mana}\n\n")
                        mainCharacter.wallet -= pickedFood[1]
                    else:
                        print("\nbroke bitch, get out")
                        break
        elif foodChoice == "2":
            print("Thanks for stopping by your local eatery")
            
            #sm.fadeout_music(1000)
            #if img_window:
             #   img_window.destroy()
            return

        else:
            print("Invalid choice")
                
                

                
            