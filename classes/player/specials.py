from colorama import Fore, Style, Back

class Special:
    def __init__(self, name, type, damage, heal, amount, manaCost):
        self.name = name
        self.type = type
        self.damage = damage
        self.heal = heal
        self.amount = amount
        self.manaCost = manaCost

    def use(self, user, target):
        """
        Returns the numeric effect of the special (damage or heal).
        """
        
        if user.mana >= self.manaCost:
            if self.heal and self.damage == True:
                target.health -= self.amount
                user.health += self.amount
                user.mana -= self.manaCost
                print(Fore.BLUE + f"New mana total:  {user.mana}" + Style.RESET_ALL)
                print(Fore.GREEN + f"New health total: {user.health}" + Style.RESET_ALL)
                return self.amount

            elif self.damage:
                target.health -= self.amount
                user.mana -= self.manaCost
                print(Fore.BLUE + f"New mana total:  {user.mana}" + Style.RESET_ALL)
                return self.amount  # return damage done
            elif self.heal:
                user.health += self.amount
                user.mana -= self.manaCost
                print(Fore.BLUE + f"New mana total:  {user.mana}" + Style.RESET_ALL)
                print(Fore.GREEN + f"New health total: {user.health}" + Style.RESET_ALL)
                return 0
            
            else:

                return 0
        else:
            print("\nsorry for party rocking :(\nYou don't have enough mana\n")
            return 0
        
    
    