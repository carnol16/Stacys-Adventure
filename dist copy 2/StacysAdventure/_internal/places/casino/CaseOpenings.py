import random
from classes.items import StoreItems
from classes.player.createPlayer import Player

#RARITY
#lower the number, the higher the rarity
blue = 90
purple = 40
pink = 20
red = 10
gold = 2

#Rarity Chart
"""
    Rarity 	    Color	    Notes
Consumer Grade	Grey/White	Most common skins.
Industrial Grad Light Blue	Uncommon skins.
Mil-Spec	    Blue	    Rare skins.
Restricted	    Purple	    Mythical skins.
Classified	    Pink	    Legendary skins.
Covert	        Red	        Ancient skins, including many weapon skins.
Exceedingly Rar	Gold	    This tier includes knives and gloves, which are even rarer than Covert skins.
Contraband	    Orange/Yellow	The rarest tier, with items like the “Howl” being the only examples.
"""

# Number of each rarity and examples
"""
blue = 5 Items
purple  = 3 Items / Weapons / Armor
pink = 3 Weapons / Armor
red = 2 Specials
gold = 1 Specials
#StoreItems("name", 4, False, True, False, True, False, amount, blue, 0) #Item EX
#StoreItems("big stick", 10, False, False, True, False, False, 10, 100, 0, True) # Weapon EX
#StoreItems("cape", 25, False, False, True, False, True, 10, 100, 0, False, True ) # Armor EX
#StoreItems("Dmyt's Ball Doctor", 200, True, False, False, True, False, 100, red, 60) #Special EX
"""


caseChoices = [ "Chroma Case"
                #"Gamma Case", 
                #"Dreams & Nightmares Case",
                #"Kilowatt Case",
                "Fever Case",
                #"CS:GO Weapon Case"
            ]

chromaOptions = (
                #BLUE ALL ITEMS
                StoreItems("Mario Mushroom", 10, False, True, False, True, False, 5, blue, 0), #heal
                StoreItems("Toe Nails", 3, False, True, True, False, False, 1, blue, 0), #damage
                StoreItems("Lolipop", 4, False, True, False, True, False, 5, blue, 0), #heal
                StoreItems("Blue Berry Muffin", 4, False, True, False, True, False, 5, blue, 0 ), #heal
                StoreItems("Spit Ball", 0, False, True, True, False, False, 2, blue, 0), #damage
                
                #PURPLE
                StoreItems("Eyeliner", 10, False, False, False, False, True, 5, purple, 0), #Armor
                StoreItems("Polly Pockets", 15, False, True, True, False, False, 10, purple, 0), #Item damage
                StoreItems("Electrical Duster", 12, False, False, True, False, False, 11, purple, 0, True), #Weapon
                
                #PINK
                StoreItems("Tazer", 53, False, False, True, False, False, 25, pink, 0, True), #pink Weapon
                StoreItems("Bikini", 46, False, False, False, False, True, 7, pink, 0), #pink Armor
                StoreItems("Crocks...but pink", 73, False, False, False, False, True, random.randint(6,7), pink, 0), #pink
                
                #RED
                StoreItems("MINONS ATTACK", 187, True, False, True, False, False, 83, red, 30), #red
                StoreItems("Dmyt's Ball Doctor", 200, True, False, False, True, False, 100, red, 60), #red
                
                #Gold
                StoreItems("Monday Night Bible Study", 300, True, False, True, False, False, 250, gold, 100), #gold
                )

"""
blue = 5 Items
purple  = 3 Items / Weapons / Armor
pink = 3 Weapons / Armor
red = 2 Specials
gold = 1 Specials
"""

feverOptions =  (
                #BLUE
                StoreItems("Rotten Tomatos", 1, False, True, False, True, False, -2, blue, 0), #blue heal
                StoreItems("Toe Nails", 3, False, True, True, False, False, 1, blue, 0), #blue damage
                StoreItems("Lolipop", 4, False, True, False, True, False, 5, blue, 0), #blue heal
                StoreItems("Blue Berry Muffin", 4, False, True, False, True, False, 5, blue, 0 ), #blue heal
                StoreItems("Spit Ball", 0, False, True, True, False, False, 2, blue, 0), #blue damage
                
                #PURPLE
                StoreItems("Spike Factory", 45, False, False, False, False, False, 21, purple, 0, True), # Weapon
                StoreItems("Bing Bong", random.randint(6, 7), False, True, False, False, False, 0, purple, 0), #Item
                StoreItems("Nacho Cheese Doritos® Locos Tacos Meal Combo", 27, False, True, False, True, False, 42, purple, 0 ), #Item Heal
                
                #PINK
                StoreItems("Grandma's Sweater", 0, False, False, False, False, True, 9, pink, 0 ), #Armor
                StoreItems("Ben 10 Watch", 50, False, False, False, False, False, random.randint(10, 50), pink, 0, True), #Weapon
                StoreItems("Wire Cutters", 12, False, False, True, False, False, 15, pink, 0, True), #pink
                
                #RED
                StoreItems("Dirty Dishes", 1, True, False, True, False, False, 40, pink, 100), #red
                StoreItems("Cat Fleas", 200, True, False, True, False, False, 6, red, 10), #red
                
                #GOLD
                StoreItems("Stacy's Spit", 400, True, False, True, False, False, 100, gold, 100), #gold
                )
"""
weaponsOptions = (
                StoreItems(), #blue
                StoreItems(), #blue
                StoreItems(), #blue
                StoreItems(), #blue
                StoreItems(), #blue
                StoreItems(), #purple
                StoreItems(), #purple
                StoreItems(), #purple
                StoreItems(), #pink
                StoreItems(), #pink
                StoreItems(), #pink
                StoreItems(), #red
                StoreItems(), #red
                StoreItems(), #gold
                )
"""
def openCase(case_name, player=None, player_return=False):
    # Map case name → tuple of options
    if case_name.lower() == "chroma case":
        options = chromaOptions
    elif case_name.lower() == "fever case":
        options = feverOptions
    else:
        print("Unknown case!")
        return

    # Spin based on rarity weights
    weights = [item.rarity for item in options]
    reward = random.choices(options, weights=weights, k=1)[0]

    print(f"YOU GOT → {reward.name} [{reward.rarity}]")

    # If a player object is passed and player_return is False, auto-store it
    if player and not player_return:
        player.quickStorage(reward)

    # If we want to return the reward to handle armor/specials/weapon
    if player_return:
        return reward
