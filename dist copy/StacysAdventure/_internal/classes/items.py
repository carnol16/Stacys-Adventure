from classes.player.armor import Armor
from classes.player.weapon import Weapon
from colorama import Fore, Back, Style


class StoreItems:

    def __init__(
        self,
        name,
        price,
        specials,
        items,
        damage,
        heal,
        armor,
        amount,
        rarity,
        manaCost,
        weapon = False,
        cosmetic = False,
        durability = None,
        addMana = False
    ):
        self.name = name
        self.price = price
        self.specials = specials
        self.items = items
        self.damage = damage
        self.heal = heal
        self.armor = armor
        self.amount = amount
        self.rarity = rarity
        self.manaCost = manaCost
        self.weapon = weapon
        self.cosmetic = cosmetic
        self.durability = durability
        self.addmana = addMana

    def use(self, user, target):
        """
        Returns the numeric effect of the special (damage or heal).
        """

        if user.mana >= self.manaCost:
            if self.damage:
                target.health -= self.amount
                user.mana -= self.manaCost
                print(Fore.BLUE + f"New mana total: {user.mana}")
                return self.amount  # return damage done
            elif self.heal:
                user.health += self.amount
                user.mana -= self.manaCost
                print(Fore.BLUE + f"New mana total: {user.mana}")
                print(Fore.GREEN + f"New health total:  {user.health}")
                return 0
            elif self.addmana:
                user.mana += self.amount
                print(Fore.BLUE + f"New mana total: {user.mana}")

            else:
                return 0
        else:
            print("sorry for party rocking :(")

    def toArmor(self):
        return Armor(self.name, self.amount)

    def toWeapon(self):
        return Weapon(self.name, self.amount)


class CaseItem:
    def __init__(self, caseName):
        self.name = caseName
        self.amount = 0

    def openCase(self, player):
        from places.casino.CaseOpenings import openCase

        # `openCase` returns a StoreItems or Special reward
        reward = openCase(self.name, player_return=True)

        # Apply the reward
        if reward.armor:
            print(f"{reward.name} is armor!")
            from classes.player.armor import Armor

            newArmor = Armor(reward.name, reward.amount)
            if player.armor:
                try:
                    player.armor.detach(player)
                except:
                    pass
            newArmor.attach(player)

        elif reward.weapon:
            print(f"{reward.name} is a weapon!")
            from classes.player.weapon import Weapon

            newWeapon = Weapon(reward.name, reward.amount)
            if player.weapon:
                try:
                    player.weapon.detach(player)
                except:
                    pass
            newWeapon.attach(player)

        elif reward.specials:
            print(f"{reward.name} is a special attack!")
            from classes.player.specials import Special

            player.attacks.append(
                Special(
                    reward.name,
                    0,
                    reward.damage,
                    reward.heal,
                    reward.amount,
                    reward.manaCost,
                )
            )

        else:
            print(f"{reward.name} added to inventory!")
            player.quickStorage(reward)

        return reward


class CraftItems(StoreItems):
    """
    A subclass of StoreItems that represents craftable items.
    Adds a list/dict of required items needed to craft it.
    """

    def __init__(
        self,
        name,
        price,
        specials,
        items,
        damage,
        heal,
        armor,
        amount,
        rarity,
        manaCost,
        required_items,
        weapon=False,
        cosmetic=False,
        durability = 100
    ):
        super().__init__(
            name,
            price,
            specials,
            items,
            damage,
            heal,
            armor,
            amount,
            rarity,
            manaCost,
            weapon,
            cosmetic,
            durability
        )

        # Required items for crafting (dict or list)
        self.required_items = required_items

    def can_craft(self, inventory):

        # Check if the player's inventory contains all needed items.

        for item_name, needed_amount in self.required_items.items():
            if inventory.get(item_name, 0) < needed_amount:
                return False
        return True

    def craft(self, inventory):

        # Check if the player has the required items
        if not self.can_craft(inventory):
            print(f"Missing materials to craft {self.name}")
            return None

        # Remove items from inventory
        for item_name, needed_amount in self.required_items.items():
            inventory[item_name] -= needed_amount

        print(f"Crafted: {self.name}")
        return self
