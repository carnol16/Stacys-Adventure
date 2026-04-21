import random
from .armor import Armor
from .specials import Special
from classes.items import StoreItems
from colorama import Fore, Back, Style
from PIL import Image
from  audioMixer import SoundManager
import images.openPicture as img
from datetime import datetime

sm = SoundManager()
class Player:

    def __init__(self, type, color, name):
        self.type = type
        self.color = color
        self.name = name
        self.mana = 50
        self.space = 10 #default space
        self.items = [] #empty storage
        self.wallet = 0
        self.weapon = None
        self.armor = None
        self.badBoy = False
        self.increaseDefend = 0
        self.partyMembers = []
        self.activeParty = None
        self.fightNum = 0

        
        

        if type == "warrior":
            self.health = 200
            self.damage = 10
            self.defense = 4
            self.space = 3
            self.attacks = [
                Special("Taco HITTER", "attack", True, False, 20, 25),
                Special("Counter Strike", "attack", True, False, 10, 10),
                Special("Children Tears", "heal", False, True, 100, 50)
            ]   

        elif type == "basement dweller":
            self.health = 150
            self.damage = 8
            self.defense = 10
            self.space = 8
            self.attacks = [
                Special("GOONING", "attack", True, False, 5, 10),
                Special("Discord Modding", "attack", True, False, 15, 25),
                Special("White Monster into the VEINS", "heal", False, True, 25, 10)
            ]   

        elif type == "boat man":
            self.health = 180
            self.damage = 10
            self.defense = 10
            self.space = 5
            self.attacks = [
                Special("Plunder", "attack", True, False, 25, 10),
                Special("Cannon BRRRRR", "attack", True, False, 100, 60),
                Special("Motorboating", "heal", False, True, 50, 40)
            ]
            
        elif type == "ninja":
            self.health = 120
            self.damage = 7
            self.defense = 15
            self.space = 1
            self.attacks = [
                Special("Sneaky Deeky Like", "attack", True, False, 10, 5),
                Special("Back Flip", "attack", True, False, 25, 25),
                Special("Drinking Blood of My enemies", "heal", True, True, 10, 30)
            ]  

        else:
            self.health = 10
            self.damage = 1
            self.defense = -10
            self.space = 2
            self.attacks = [
                Special("depression", "attack", True, False, -10, 10)
            ]  

        if color == "blue":
            self.health += 10

        elif color == "red":
            self.health -= 8
            self.damage += 2
            
    def getPlayerDict(self):
        """Returns a dictionary containing all instance variables."""

        return self.__dict__
    
    def leaderboardPost(self, fightNum):
        return {
            "name": self.name,
            "type": self.type, # or whatever your attribute is
            "fight_number": fightNum, # <--- This MUST match the sort key
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def myStats(self):
        avalibleSpace = self.space - len(self.items) 
        print(f"Here is {self.name}'s silly stats\n")
        
        print(Fore.GREEN + f"Health: {self.health}")
        print(Fore.BLUE + f"Mana: {self.mana}")
        if self.armor is None:
            print(Fore.WHITE + f"Base Defense: ", self.defense)
            print("Armor: None")
        else:
            print(f"Base Defense: ", self.armor.amount)
            print(f"Armor: {self.armor.name} || DEF: +{self.armor.amount} || DUR: {self.armor.durability}")
        if self.weapon is None:
            print(Fore.RED + f"Base Damage: ", self.damage)
            print("Weapon: None")
        else:
            print(Fore.BLUE + f"Base Damage:  {self.damage - self.weapon.amount}")
            print(Fore.RED + f"Weapon: {self.weapon.name} || DMG: +{self.weapon.amount}")
            print(Fore.RED + f"Total Damage: {self.damage + self.weapon.amount}")
        print(f"Available Space {avalibleSpace}\n")
        if self.activeParty != None:
            print(f"Party Member: {self.activeParty.name}", Fore.GREEN + f"Health: {self.activeParty.health}" )
        else:
            print("Party Member: You a loner lol")

    def attack(self, success, option, enemy):
        choice = option
        base = self.damage

        if choice == "1":
            if success % 2 == 0:
                if random.random() < 0.2:
                    print("\nYOU HIT A CRIT!!!")
                    return int(base * 1.5)
                return base
            else:
                return 0  # Attack missed

        elif choice == "2":
            counter = 0
            for i in self.attacks:
                def colorPick():
                    if i.type == "attack":
                        return Fore.RED
                    elif i.type == "heal":
                        return Fore.GREEN
                    elif i.type == "attack" and "heal":
                        return Fore.MAGENTA
                    else:
                        return Fore.WHITE
                if i.type == "attack":
                    typeName = "DMG"
                elif i.type == "heal":
                    typeName = "Health"
                print(Fore.WHITE + f"{counter}: ", Fore.YELLOW + f"{i.name}", Fore.WHITE + "||", Fore.BLUE + f"Cost: {i.manaCost}", Fore.WHITE + "||" ,  colorPick() + f"+{i.amount} {typeName}")
                counter += 1
                
            try:
                specialChoice = int(input(Fore.WHITE + "\nWhich special do you wanna useeeeeee? "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                return 0

            if not (0 <= specialChoice < len(self.attacks)):
                print("Invalid special choice.")
                return 0

            # FIXED: use(self, enemy) instead of mainCharacter, enemy
            dmg = self.attacks[specialChoice].use(self, enemy)
            return dmg

        elif choice == "3":
            counter = 0
            itemCount = len(self.items)
            if itemCount > 0:
                for i in self.items:
                    def colorPick():
                        if i.type == "damage":
                            return Fore.RED
                        elif i.type == "heal":
                            return Fore.GREEN
                        elif i.type == "attack" and "heal":
                            return Fore.MAGENTA
                    print(counter, i.name)
                    counter += 1
                try:
                    itemChoice = int(input("\nwhich item do you wanna useeeeeee? "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    return 0

                if not (0 <= itemChoice < len(self.items)):
                    print("Invalid item choice.")
                    return 0

                # FIXED: use(self, enemy)
                self.items[itemChoice].use(self, enemy)

                del self.items[itemChoice]
                return 0
            else:
                print("\nwasted a turn dumbass")
                return 0
        elif choice == "4":
            extraDefense = random.randint(1, 8)
            print("\nAhhhhhh you scared huh")
            print(f"This round: DEF +{extraDefense}")
            self.increaseDefend = extraDefense
            
            return 0
        else:
            print("")
            return 0
        
    def defend(self, success, incomingDamage):

        # Safety check: no armor equipped
        if self.armor is None:
            return incomingDamage
        elif self.increaseDefend == 0:
            # Dodge chance
            if success % 2 == 0:
                if random.random() < 0.1:
                    print("\nGOOD DODGE!!!")
                    return 0

                #Damage reduction
                reducedDamage = incomingDamage - self.defense
                reducedDamage = max(reducedDamage, 1)

                # Armor durability logic
                if self.armor.durability is None:
                    self.armor.durability = 100

                durabilityLoss = int((reducedDamage / 3) - 1)
                if durabilityLoss < 1:
                    durabilityLoss = 1

                self.armor.durability -= durabilityLoss

                # Prevent negative durability
                if self.armor.durability <= 0:
                    self.armor.durability = 0
                    print(f"\n{self.armor.name} broke!")
                    self.armor.detach(self)
                    #self.items.remove(self)

                return reducedDamage

        elif self.increaseDefend > 0:
            # Dodge chance
            if success % 2 == 0:
                if random.random() < 0.1:
                    print("\nGOOD DODGE!!!")
                    return 0

                #Damage reduction
                reducedDamage = incomingDamage - self.defense - self.increaseDefend
                reducedDamage = max(reducedDamage, 1)

                # Armor durability logic
                if self.armor.durability is None:
                    self.armor.durability = 100

                durabilityLoss = int((reducedDamage / 3) - 1)
                if durabilityLoss < 1:
                    durabilityLoss = 5

                self.armor.durability -= durabilityLoss

                # Prevent negative durability
                if self.armor.durability <= 0:
                    self.armor.durability = 0
                    print(f"\ns{self.armor.name} broke!")
                    self.armor.detach(self)
                    
                self.increaseDefend = 0

                return reducedDamage
        # No dodge / odd success → full damage 
        return incomingDamage
   
    def storage(self):

        
        imagePath = r"images/storage.jpg" 
        img_window = img.openIMG(imagePath)
        sm.play_music("storage")


        while True:

            print(Fore.WHITE + "")
            print(Back.LIGHTCYAN_EX + "===== STORAGE MENU ===== " + Back.RESET)
            print(Back.LIGHTBLUE_EX + "1. Check Stats           " + Back.RESET)
            print(Back.LIGHTBLUE_EX + "2. Remove item           " + Back.RESET)
            print(Back.LIGHTBLUE_EX + "3. View all items        " + Back.RESET)
            print(Back.LIGHTBLUE_EX + "4. Use an item           " + Back.RESET)
            print(Back.LIGHTBLUE_EX + "5. Attach / Detach Armor " + Back.RESET)
            print(Back.LIGHTBLUE_EX + "6. Attach / Detach Weapon" + Back.RESET)
            print(Back.LIGHTBLUE_EX + "7. Exit storage          " + Back.RESET)

            choice = input("> ").strip()

            # 1. CHECK SPACE
            if choice == "1":
                self.myStats()
                

            # 2. REMOVE ITEM
            elif choice == "2":
                if not self.items:
                    print("Storage is empty!")
                    continue
                
                print("\nItems:")
                for i, item in enumerate(self.items):
                    print(f"{i}: {item.name}")

                try:
                    idx = int(input("Enter index to remove: "))
                    removed = self.items.pop(idx)
                    print(f"Removed {removed.name}")
                except:
                    print("Invalid index")


            # 3. VIEW ALL ITEMS
            elif choice == "3":
                if not self.items:
                    print("Storage empty!")
                else:
                    print("\nYour Items:")
                    for i, item in enumerate(self.items):

                        if getattr(item, "armor", False):
                            kind = "Armor"
                        elif getattr(item, "weapon", False):
                            kind = "Weapon"
                        else:
                            kind = "Item"

                        # Show durability for armor
                        if kind == "Armor":
                            durability = getattr(item, "durability", "N/A")
                            print(f"{i}: {item.name} ({kind}) - Durability: {durability}")
                        else:
                            print(f"{i}: {item.name} ({kind})")



            # 4. USE ITEM (consumables)
            elif choice == "4":
                if not self.items:
                    print("No items to use!")
                    continue

                print("\nWhich item do you want to use?")
                for i, item in enumerate(self.items):

                    print(Fore.GREEN +  f"{i}: {item.name}, +{item.amount}")

                try:
                    idx = int(input("Choose index: "))
                    item = self.items[idx]

                    if item.heal:
                        item.use(self, self)  # You may need target = enemy in battle
                        print(f"Used {item.name}")
                        self.items.pop(idx)
                    else:
                        print("This isn't a usable item!")
                except:
                    print("Invalid selection.")

            # 5. ATTACH/DETACH ARMOR
            elif choice == "5":
                print("\n===== ARMOR MENU =====")

                # If player wearing armor
                if self.armor:
                    print(f"Currently equipped armor: {self.armor.name} (+{self.armor.amount} DEF)")
                    det = input("Detach current armor? (yes/no): ").lower()
                    if det == "yes":
                        old = self.armor
                        self.defense -= old.amount
                        self.armor = None
                        self.quickStorage(old)
                        print(f"Detached {old.name} and stored it.")
                    continue

                # If not wearing armor → pick one from storage
                print("\nSelect armor to attach:")
                armor_items = [(i, item) for i, item in enumerate(self.items) if getattr(item, "armor", False)]

                if not armor_items:
                    print("You have no armor in storage.")
                    continue

                for i, item in armor_items:
                    print(f"{i}: {item.name} (+{item.amount} DEF)")

                try:
                    idx = int(input("Choose armor index: "))
                    newArmor = self.items.pop(idx)

                    self.armor = newArmor
                    self.defense += newArmor.amount
                    print(f"Equipped {newArmor.name}!")
                except:
                    print("Invalid selection.")

            # 6. ATTACH/DETACH WEAPON
            elif choice == "6":
                print("\n===== WEAPON MENU =====")

                if self.weapon:
                    print(f"Equipped weapon: {self.weapon.name} (+{self.weapon.amount} DMG)")
                    det = input("Detach current weapon? (yes/no): ").lower()
                    if det == "yes":
                        old = self.weapon
                        self.damage -= old.amount
                        self.weapon = None
                        self.quickStorage(old)
                        print(f"Detached {old.name} and stored it.")
                    continue

                print("\nChoose weapon to attach:")
                weapon_items = [(i, item) for i, item in enumerate(self.items) if getattr(item, "weapon", False)]

                if not weapon_items:
                    print("You have no weapons in storage.")
                    continue

                for i, item in weapon_items:
                    print(f"{i}: {item.name} (+{item.amount} DMG)")

                try:
                    idx = int(input("Choose weapon index: "))
                    newWeapon = self.items.pop(idx)

                    self.weapon = newWeapon
                    self.damage += newWeapon.amount
                    print(f"Equipped {newWeapon.name}!")
                except:
                    print("Invalid selection.")

            # 7. EXIT
            elif choice == "7":
                print("Exiting storage.")
                img.openIMG(destroy=True)
                sm.fadeout_music(1500)  # fade out over 1.5 secs
                break

            else:
                print("Invalid choice, try again.")
           
    def quickStorage(self, addItem):
        freeSpace = self.space - len(self.items)
        if freeSpace > 0:
            self.items.append(addItem)
            print("SPACE:", self.space, "CURRENT ITEMS:", len(self.items))
        else:
            print("sorry baddie, no space")
            dropItem = input("would you like to dispose of something??? ")
            
            if dropItem == "yes":
                print("Here are the items you have currently:")
                for i in self.items:
                    print(i.name)

                item = input("Enter the item to remove: ").strip()
                if item in self.items:
                    self.items.remove(item)
                    print(f"{item} removed. Current items: {self.items}")
                else:
                    print(f"{item} not found in storage.")
                
                self.items.append(addItem)
                
            else:
                print("your loss:( ")    
    
    def hasItem(self, itemName):
        for item in self.items:
            if item.name == itemName:
                return True
        return False    

      

class NPC(Player):
    def __init__(self, npc_type, color):
        # Prevent Player.__init__ from overwriting NPC stats
        super().__init__("npc", color, npc_type)

        self.npc_type = npc_type

        # Assign NPC-specific stats
        if npc_type == "Monty":
            self.health = 100
            self.maxHealth = 100
            self.damage = 5
            self.defense = 5

            # Monty's attack list
            self.attacks = [ 
                            Special("CM Punk UFC Type Move ", "attack", True, False, 10, 0), 
                            Special("Super Soaker 9000", "attack", True, False, 45, 0)
                            ]

        elif npc_type == "Parim the Iguana":
            self.health = 60
            self.maxHealth = 60
            self.damage = 0
            self.defense = 5
            # Parim is healer
            self.attacks = [ 
                            Special("Kisses from the Overlords", "attack", True, False, 24, 0), 
                            Special("Licks from the Posseum", "attack", True, False, 12, 0)
                            ]

        # Anything else defaults to harmless NPC
        else:
            self.health = 50
            self.maxHealth = 50
            self.damage = 1
            self.defense = 0
            self.attacks = []

    # -------------------------
    # NPC DECISION SYSTEM
    # -------------------------

    # Ensure signature matches Player.attack
    def attack(self, enemy, mainCharacter):
        return self.chooseAction(enemy, mainCharacter)

    def chooseAction(self, mainCharacter, enemy):
        # Monty = DPS AI
        if self.npc_type == "Monty" or "Parim the Iguana":
            attack_moves = [sp for sp in self.attacks if sp.type == "attack"]
            if attack_moves:
                # FIXED: random.choice avoids index crashes
                return random.choice(attack_moves).use(self, enemy)

        # Parim = healer AI
        if self.npc_type == "korean BBQ":
            heal_moves = [sp for sp in self.attacks if sp.type == "heal"]

            # Heal main character if needed
            if mainCharacter.health < mainCharacter.maxHealth * 0.7 and heal_moves:
                return random.choice(heal_moves).use(self, mainCharacter)

            # Otherwise attack
            attack_moves = [sp for sp in self.attacks if sp.type == "attack"]
            if attack_moves:
                return random.choice(attack_moves).use(self, enemy)

        # Default behavior: basic attack (if exists)
        attack_moves = [sp for sp in self.attacks if sp.type == "attack"]
        if attack_moves:
            return random.choice(attack_moves).use(self, enemy)

        return 0  # NPC does nothing



