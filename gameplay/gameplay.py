import random
import socket
import json
import datetime
import time
import textwrap
from colorama import Fore, Back, Style
from classes.enemy import Enemy, Boss
from classes.player.armor import Armor
from classes.player.weapon import Weapon
from places.casino.CasinoOpen import openCasino
from places.blacksmith.BlackSmithOpen import openBlacksmith
from classes.player.createPlayer import Player
from audioMixer import SoundManager
from classes.items import StoreItems
from places.restaurant.restaurantOpen import openResturant
from classes.player.createPlayer import NPC
import threading
import images.openPicture as img

class BattleDJ(threading.Thread):
    def __init__(self, sound_manager, clips):
        super().__init__()
        self.sm = sound_manager
        self.clips = clips
        self.running = True
        self.daemon = True  # Ensures audio stops if the main game exits

    def run(self):
        while self.running:
            clip = random.choice(self.clips)
            self.sm.play_music(clip)
            # Sleep in small increments so thread exits quickly on stop()
            for _ in range(49):
                if not self.running:
                    break
                time.sleep(0.1)

    def stop(self):
        self.running = False

# SETTINGS
line_width = 70       # wrap width
delay = 0.075         # delay per character
line_delay = 0.15     # delay between lines

def has_internet():
    print("Checking internet connection...")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("Internet detected: Online mode")
        return True
    except OSError:
        print("No internet detected: Offline mode")
        return False

intChoice = input("Would you like to use online features(y/n)?\n>")
if intChoice.lower() == "y":
    if has_internet():
        from places.store.StoreOpen import openStore
    else:
        from places.store.StoreOpenOffline import openStore
else:
    from places.store.StoreOpenOffline import openStore
    

sm = SoundManager()

battleMusic = [f"out{i:03d}" for i in range(753)]
story = """
In the pastel-paved suburb of Lollipop Circle, a place where gumdrop mailboxes cheerfully wave at passersby and street lamps occasionally sparkle with glitter, lived Stacy—a towering goth girl with a heart big enough to hug a dragon and eyeliner sharp enough to slice a villain in half.
Her neighbors were used to seeing her stomp down the sidewalk in her platform boots, black dress swishing like a storm cloud trying very hard to be dramatic in a place where even the grass smelled faintly of cotton candy.
But today—oh today—Stacy was on a mission.

The Magical Stacy’s Mom (a mysterious artifact shaped like a glowing heart with overwhelmingly MILF-like energy for reasons no one fully understands) had been targeted by a long list of villains:
The Bubblegum Bandit…
Sir Smooch-A-Lot…
Mistress Glitterdoom…
The Swole Necromancer of Flexington…
And like twelve more weirdos.

Stacy couldn’t defend it alone.

She needed a mans!!!
Not just any mans…
A heroic mans…
A cute mans…
A mans who could lift heavy things and maybe her too.
A mans who respected a girl with black lipstick and a scythe collection.

Thus began her flirt-fueled recruitment tour.
"""


# FUNCTION TO SCROLL TEXT
def type_line(text):
    for char in text:
        chosenColor = random.choice([Fore.WHITE, Fore.GREEN, Fore.BLUE, Fore.RED, Fore.MAGENTA])
        print(chosenColor + char, end='', flush=True)
        time.sleep(delay)
    print()  # new line
    time.sleep(line_delay)

def characterBuildIntro():
    sm.play_music("STACYMOM")
    wrapped = textwrap.fill(story, width=line_width)
    for line in wrapped.split('\n'):
        type_line(line)

    print( Fore.WHITE + 
    r"""
:%    @*++++++++@  .@                                                                
                                      @: @        @   @=:-*%*:         :*#=* %                                                              
                                    @ %=+% =   @ @==#+:                    .=  @                                                            
                                 @  %-:  -@  @ +-:                           -% @   @    #                                                  
                               @ +-:.    : @ @@*:                   ..--:.    - :%  %::-::#  %                                              
                             *  -       .*      :          .-++-.  .+ *  +.    =  : +     .=+# @                                            
                           =  +:        : # + #-:   -=: -*##    -  : #  @ +    .  # =         +                                             
                          @ +.         :# % #:..=+-+  .=+   =@ :*..:@    @ -    # % :         ::                                            
                        * :.          :* * #=--*  #@     @+ :  @ **        @ -. %  =           + #                                          
                       *.=.          .* @  *.  =      = @   @   @  :        @ +.@  =           :-@ *                                        
                      @ =           .+ #   ..*@@     @@    @     +            @ @  =             :                                          
                     * *:          :+ -  @=-+     @@@           @@@@@@#         %  *              .=                                        
                    + *:           + %=   -#    @  @          @ @     .+-@@@ @ # * =                + @                                     
                     *.            +   %@ *    @   +          @   #    @   = @ # =-:                 - @                                    
                   @ :             .=+-+ =@    @@  @          @  @@ =. *   * + @: :                   : :                                   
                    -                 - . *    @  @@          @   @    +   @%@ @ @=                    .-                                   
                  @*. ..-..           * @ %    @  @           @#  @ =@ @       @  -                      * @                                
                 @ +-=  :             @ %  @    #     :         @@    %    @      ..                     .=                                 
                @ @=  .= =.           @ @    @%       @                  @       %- =.                     = @                              
              @@@*-  #  :.            + =  @@  @ %@   @        @@   @  @@        @ + *:                     = @                             
                   +  =:              --@ %  @@  *   @         #  @@  @@        @   % +.                    :+ @                            
                ++  +:                  +                                      @     @ =                      = %                           
             :# #==-                 :=@ %        @@@@@@@@@@@-                @       @ +.                .:+:=:+                           
          +#  #-:                  ::@ =-+*       @          +=             @          @ -                . - .:-* @                        
       @@ @=+=                   .:@ @     @         @@@@@@@#            #@             %=.               .+ -- =*@ #                       
    @# #=-:                     .: @        @+                         @@                 *.               .:   =+ @* @                     
  @ *=-:                       - @            @:                   @@-                   +  .                 = -                           
 - +.                        :+ @               %@             .@@.   @                   - +                 .-  @                         
 %-.                        .* #                @  @@#      @@*      @                        .                 :-# @                       
 .                         .+ ..                @      @@@-          @                      @ =                   .:# +                     
                          .+ @             @@  @:                    @                       @ :                    .-  @-                  
                       :-=# @          @@.       @                    @                        #.                      .*  @                
                  -*#=-% %*          @            @                 @= #@=                    @ *:                      :==%  @@            
         .=##+--  #  :%         -@@*  @            @            =@#        @@                  @ =                         :=+:+    ---=%.  
       -=#    ::-            @@        @@           @       @@#            @  @@                @ -.                           :+#+-:...:-  
     :*  +                 @%            @          @    @@             @@       @=              # =                                     :- 
   :- -:                 -@                @         -%@             -@:            @             % +:                                      
 -% =                   @                  *-         :            @@                 @*           @  -.                                    
  @                   @                      @       #           @                      @@           @ +.                                   
 =                  @                         @      @        #@                            @         -* *=-                                
                  @                            @     @      @@                                @         #@  +:=#@*-                        
               @@                              @     @   .@                                     *@          =*    @+:. =---:::=*%+- ..      
         .==@@                                  @    @ +@                                          @@-                      *     @#- +::   
   @+*@ +   @                  @*                @   @=                                                @@                             @  *- 
  @     :    @               -@                  @-@@                            :                        @@=                           +   
  @     @    -+           #@@.                                                   @ @@@*                    @  @#                            
 @*     @     @       :@@   @                                                   #       @*               @     @@@@@@@.                     
        @     @  @@@       *                                                   @          @@           @      @       @                     
  +@@  @%@@@@@@            #                                                   %             @%       =:      #      @                      
  %     =%                  @                                                 +                 @%    @      @          @                   
       @   @                 %                    @                           @                    @@@      @             @                 
  @   %@@  @                  @                   :                           @                      @ *###.=%      @* =@@                  
                                @                                             @                             @                               
                                  @@.            %@                           @                             @    @%*@@                      
                                                  =@                          *                             =   @                           
                                       @            @@                     @  -                              @@                             
                                        @              @@@             *@@  .:                                                              
                                          @                 *@@@@@@@@#      *                                                               
                                           %                               @                                                                
                                           @                              @                                                                 
                                           @                             @                                                                  
                                           @                             @                                                                  
                                          @                              @                                                                  
                                         @                                @                                                                 
                                        @                                  @                                                                
                                      #-                                    @+                                                              
                                    @@  *@@@@@@@@#                            @  -                                                          
                               @@@                 @@@@               #@@@@@@@+@                                                            
                           +@@                                      .           @                                                           
                        @@                                                       @                                                          
                       @                                                         +-                                                         
                     @.                                                           @                                                         
                    @                                                              +                                                        
                   @                                                               @                                                        
                  @                                                                 @                                                       
                 @                                                                  @                                                       
                 @                                                                  =.                                                      
                @                                                                    @                                                      
               @                                                            =@       @                                                      
               @                  .                       =                  @       +                                                      
              -                  @                        +#                 #        @                                                     
              @                @.                          :@                         @                                                     
             @                @                              @                @       @                                                     
             .               @                                #               @       @                                                     
            @       @                 @@@#@                    @              :       @                                                     
            @       @                @    @                     @             %       @                                                     
           .       +@                @    @                                   #       @                                                     
           @      #@                 @    @      :@@%@                         @      @                                                     
           :    @= @                 .*   @    @                               @      @                                                     
          @@ .@.   @-#%=              @   @  @        @         #@*                   @                                                     
             @            +@@@@@     - *@#@@           @     -@=  =                   @                                                     
           =:                    @ @@%-    @            @: =@      @                  @                                                     
          ==                               @             .          @.                +                                                     
         =:                                *                             :@@@*#####**-@@                                                    
         @                                 +             @                           -                                                      
        @                                   -            @                           @                                                      
        @                                   +             %                           @                                                     
        +                                   +             @                            :                                                     
       @                                    +              *                           -                                                     
       @                                    +              -+                          :   
"""
)


    """
    # Hey my fellow baddie. I'm Stacy. The big titty goth girl at your service
    """
    print("Hey my fellow baddie. I'm Stacy. The big titty goth girl at your service I'm Stacy.")
    name = input("Welcome to the silly land of Lollipop Circle!!! What is your name: ")

    if len(name) <= 5:
        print(Fore.WHITE + "thats a good name, great choice\n")
    elif len(name) <= 10:
        print("Not a great choice but it will do\n")
    else:
        print("ew... you are going by Jerry now.\n")
        name = "jerry"

    print()
    playerType = input(
        "Alright "
        + name
        + ". Now what kind of character would you like to be?\nYou can be a warrior, basement dweller, boat man, or ninja... or something else i guess: "
    )

    playerType = playerType.lower()

    if playerType in ("warrior", "basement dweller", "boat man", "ninja"):
        print("Niceeeeee. You really know your stuff", name)
        print("You will make a great", playerType)
    else:
        print("damn you really gotta be like this huh, couldn't be normal...")
        print("enjoy being a", playerType, "i guess...\n")

    print()

    color = input("We are almost ready now!!! I now just need your favorite color: ")
    color = color.lower()

    print("Perfect, this is just something a little silly!! No worries")
    print(color + " is amazing\n")

    print("Now we are ready for our little journey!")

    sm.fadeout_music(1000)  
    return Player(playerType, color, name)


def leaderboardPost(mainCharacter, fightNum):
    print(f"You got to fight number: {fightNum}!!!")
    postChoice = input("Would you like to post this to the leader board?")

    
    entry = Player.leaderboardPost(mainCharacter, fightNum)
    try:
        with open('leaderboard.json', 'r') as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = []
    leaderboard.append(entry)
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f, indent=4)
    
    # Display leaderboard
    leaderboard.sort(key=lambda x: x['fight_number'], reverse=True)
    print("\nTop 5 Leaderboard:")
    for i in range(min(5, len(leaderboard))):
        e = leaderboard[i]
        print(f"{i+1}. {e['name']} ({e['type']}) - Fight {e['fight_number']} on {e['date']}")
    
    # Find current player's rank
    for rank, e in enumerate(leaderboard, 1):
        if (e['date'] == entry['date'] and 
            e['name'] == entry['name'] and 
            e['type'] == entry['type'] and 
            e['fight_number'] == entry['fight_number']):
            print(f"\nYour position: {rank}. {e['name']} ({e['type']}) - Fight {e['fight_number']} on {e['date']}")
            break

def enemyBattle(mainCharacter, fightNum, part):
    
    dj = BattleDJ(sm, battleMusic)
    dj.start()

    enemy_types = ("goblin", "snake", "turtle", "log", "Razer DAWG")
    enemy_name = random.choice(enemy_types)
    enemy = Enemy(enemy_name)
    partyMember = mainCharacter.activeParty
    enemy.health = enemy.health * part

    print("\nEnemy #" + str(fightNum + 1) + ": " + enemy_name)

    turn = 1
    print(Fore.GREEN + "Current Health: ", mainCharacter.health)
    print(Fore.BLUE + "Current Mana: ", mainCharacter.mana)

    # Battle LOOP
    
    while enemy.health > 0 and mainCharacter.health > 0:

        if turn % 2 == 0:
            # Enemy attacks
            success = random.randint(0, 100)
            dmg = enemy.attack(success)
            if mainCharacter.activeParty == None:  
                reduce = mainCharacter.defend(success, dmg)

                mainCharacter.health -= reduce
                #mainCharacter.armor.durablity -= 1
                if mainCharacter.health <= 0:
                    print(Fore.WHITE + f"Enemy hits you for {reduce}! {mainCharacter.name}'s HP = 0")
                else:
                    print(Fore.WHITE + f"Enemy hits you for {reduce}! {mainCharacter.name}'s HP = {mainCharacter.health}")
            elif mainCharacter.activeParty != None:
                pickedTarget = random.choice([mainCharacter, partyMember])
                print(f"{enemy_name} chose {pickedTarget.name}")
                reduce = pickedTarget.defend(success, dmg)

                pickedTarget.health -= reduce
                #mainCharacter.armor.durablity -= 1
                if pickedTarget.health <= 0:
                    print(Fore.WHITE + f"Enemy hits {pickedTarget.name} for {reduce}! {pickedTarget.name} HP = 0")
                else:
                    print(Fore.WHITE + f"Enemy hits {pickedTarget.name} for {reduce}! {pickedTarget.name} HP = {pickedTarget.health}")
                
            

        else:
            # Player attacks
            
            if mainCharacter.activeParty != None:
                partyMember.attack(enemy, mainCharacter)

            success = random.randint(0, 10)
            print(Fore.WHITE + "")
            print(Back.RED + "===== Battle Menu =====" + Back.RESET)
            print(Back.RED + "1. Base Attack         " + Back.RESET)
            print(Back.RED + "2. Special Attack      " + Back.RESET)
            print(Back.RED + "3. Use Item            " + Back.RESET)
            print(Back.RED + "4. Defend.             " + Back.RESET)
            
            choice = input("> ").strip()
            print("")

            if choice not in ("1", "2", "3", "4"):
                print("\nwasted a turn because you can't read smh")

                
            else:
                dmg = mainCharacter.attack(success, choice, enemy)

                reduce = enemy.defend(success, dmg)
                enemy.health -= reduce
                
                if enemy.health <= 0:
                    print(f"\nYou hit {enemy_name} for {reduce}! Enemy HP = 0")
                else:
                    print(f"\nYou hit {enemy_name} for {reduce}! Enemy HP = {enemy.health}")

            
            

        turn += 1

        if mainCharacter.health <= 0:
            print("\n\n\nGAME OVER!")
            leaderboardPost(mainCharacter, fightNum)
            img.openIMG(destroy=True)
            exit()
        if mainCharacter.activeParty != None:
            if partyMember.health <= 0:
                print(f"{partyMember.name} has died:(\nThey have been removed from party")
                mainCharacter.activeParty = []
    print("\nCongrats!!! You defeated the", enemy_name)

    # GET THE DROP
    if mainCharacter.badBoy == False:
        mainCharacter.wallet += random.randint(0, 15)
        itemDropped = enemy.getDrop()

        if itemDropped == "gold":
            mainCharacter.wallet += random.randint(5, 30)

        else:
            print(f"{enemy.kind} dropped {itemDropped.name}\n")

            # If item is armor, convert it
            if itemDropped.armor:
                print(f"{itemDropped.name} is armor!")

                equip = input("Do you want to equip it now? (yes/no): ").lower()

                if equip == "yes":
                    newArmor = Armor(itemDropped.name, itemDropped.amount)

                    # remove old armor bonus if exists

                    if mainCharacter.armor:
                        mainCharacter.armor.detach(mainCharacter)

                    newArmor.attach(mainCharacter)
                    # skip storage
            elif itemDropped.weapon:
                print(f"{itemDropped.name} is weapon!")

                equip = input("Do you want to equip it now? (yes/no): ").lower()

                if equip == "yes":
                    newWeapon = Weapon(itemDropped.name, itemDropped.amount)

                    # remove old armor bonus if exists

                    if mainCharacter.weapon:
                        mainCharacter.weapon.detach(mainCharacter)

                    newWeapon.attach(mainCharacter)
                    # skip storage
            else:

                addStorage = input("would you like to put this in your inventory (yes/no): ")

                if addStorage.lower() == "yes":
                    mainCharacter.quickStorage(itemDropped)

                elif addStorage.lower() == "no":
                    print("okayyyyyy")

                else:
                    print("dumb ass bitch can't say yes or no...")
                    print(
                        "You can't get a item drop, monkey money, or baddies next fight"
                    )
                    mainCharacter.badBoy = True
    else:
        print("WOMP WOMP!\nShouldn't have been a bad boy" + mainCharacter.name)

    dj.stop()
    sm.fadeout_music(1000)
    dj.join()  # Wait for the audio thread to finish
    mainCharacter.health += 10
    mainCharacter.mana += 15
    fightNum += 1
    return fightNum

def bossBattle(mainCharacter, fightNum, part):
    
    dj = BattleDJ(sm, battleMusic)
    dj.start()
    if part == 5:
        mult = part
        enemy = Boss("STACY'S MOM",fightNum)
        if mainCharacter.hasItem("Bing Bong"):
            print("Player has Bing Bong!\nNow that means you get something silly")
            
            mainCharacter.health = mainCharacter.health + 150
            print(f"You got 150 HP!!!\nNew total health: {mainCharacter.health}")
            
            #New Weapon
            old = mainCharacter.weapon
            mainCharacter.damage -= old.amount
            mainCharacter.weapon = None
            mainCharacter.quickStorage(old)
            print(f"Detached {old.name} and stored it.")
            
            newWeapon = StoreItems("BLOWDART OF DOOM", 100, True, False, True, False, False, 500, 10, 0, True)
            mainCharacter.weapon = newWeapon
            mainCharacter.damage += newWeapon.amount
            print(f"Equipped {newWeapon.name}!")

    else:
        mult = part
        enemy_types = ("Carl", "BENJAMIN", "Stacy")
        enemy_name = random.choice(enemy_types)
        enemy = Boss(enemy_name, fightNum)

    print("\nBoss #" + str(fightNum / 5) + ": " + enemy_name)

    turn = 1
    print("Current Health: ", mainCharacter.health)
    print("Current Mana: ", mainCharacter.mana)

    # Battle LOOP
    while enemy.health > 0 and mainCharacter.health > 0:

        if turn % 2 == 0:
            # Enemy attacks
            success = random.randint(0, 100)
            if success % 4 == 0:
                dmg = Boss.attackBoss(enemy) * part
            else:
                dmg = Boss.attack(enemy, success)
            
            dmg  *= mult
            reduce = mainCharacter.defend(success, dmg)

            mainCharacter.health -= reduce
            # mainCharacter.armor.durablity -= 1

            print(f"Enemy hits you for {reduce}! Your HP = {mainCharacter.health}")

        else:
            # Player attacks
            success = random.randint(0, 10)
            print(Fore.WHITE + "")
            print(Back.RED + "===== Battle Menu =====" + Back.RESET)
            print(Back.RED + "1. Base Attack         " + Back.RESET)
            print(Back.RED + "2. Special Attack      " + Back.RESET)
            print(Back.RED + "3. Use Item            " + Back.RESET)
            print(Back.RED + "4. Defend.             " + Back.RESET)
            
            choice = input("> ").strip()
            print("")

            if choice not in ("1", "2", "3", "4"):
                print("\nwasted a turn because you can't read smh")

                
            else:
                dmg = mainCharacter.attack(success, choice, enemy)
                
                dmg *= mult
                reduce = enemy.defend(success, dmg)
                enemy.health -= reduce

                print(f"\nYou hit {enemy_name} for {reduce}! Enemy HP = {enemy.health}")

        turn += 1

        if mainCharacter.health <= 0:
            print("GAME OVER!")
            leaderboardPost(mainCharacter, fightNum)
            img.openIMG(destroy=True)
            exit()
    print("Congrats!!! You defeated the", enemy_name)

    # GET THE DROP
    if mainCharacter.badBoy == False:
        mainCharacter.wallet += random.randint(10, 30)
        itemDropped = enemy.getDrop()

        if itemDropped == "gold":
            mainCharacter.wallet += random.randint(5, 30)

        
        else:
            mainCharacter.attacks.append(itemDropped)



    mainCharacter.health += 10
    mainCharacter.mana += 15
    fightNum += 1
    dj.stop()
    dj.join()
    sm.fadeout_music(1000)
    return fightNum

def postCombat(mainCharacter):
    # STOP TIME
    print("\n\nYou currently have", mainCharacter.wallet, "monkey money")

    if mainCharacter.badBoy == False:
        while True:
            print("\n===== POST FIGHT MENU =====")
            print("1. BIG TOP")
            print("2. Casino")
            print("3. Blacksmith")
            print("4. Storage")
            print("5. Restraurant")
            print("6. Next Fight")

            stop = input("> ").strip()

            if stop.lower() == "1":
                openStore(mainCharacter)
                    
                continue

            elif stop.lower() == "2":
                openCasino(mainCharacter)

                continue
            
            elif stop.lower() == "3":
                openBlacksmith(mainCharacter)

                continue
            
            elif stop.lower() == "4":
                mainCharacter.storage()

                continue
            
            elif stop.lower() == "5":
                openResturant(mainCharacter)

                continue

            elif stop.lower() == "6":
                print("\nYou continue your journey...\n\n")
                img.openIMG(destroy=True)
                break

            else:
                print("\nDumb ass bitch can't say a real option...")
                print("You can't get an item drop, gold, or baddies next fight.\n\n")
                mainCharacter.badBoy = True
                break

    else:
        print("\nYOU THOUGHT! Hope you learned your lesson silly goose.\n\n")
        mainCharacter.badBoy = False
        

def npcGrab(mainCharacter):
    npcType = ["Monty", "Parim the Iguana",]
    
    npcPicked = random.choice(npcType)

    newPartyMember = NPC(npcPicked, "blue", npcPicked)
    
    print(f"{newPartyMember.name} has joined your party!!!")
    print(f"Here is {newPartyMember.name}'s stats!\n")
    newPartyMember.myStats()
        
    if mainCharacter.activeParty == None:
        mainCharacter.activeParty = newPartyMember
    else:
        choice = input(f"Would you like to make {newPartyMember.name} active? (y/n)\n>")
        
        if choice.lower() == "y":
            mainCharacter.activeParty.append(mainCharacter.activeParty)
            mainCharacter.activeParty = newPartyMember
            
        elif choice.lower() == "n":
            mainCharacter.partyMembers.append(newPartyMember)
    
    
    npcType.remove(npcPicked)
    
