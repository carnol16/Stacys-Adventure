class Weapon:
    tempAmount = 0
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount   # amount = defense bonus
        self.weapon = True
        self.armor = False
        
    def toStoreItem(self):
        from classes.items import StoreItems
        return StoreItems(
            self.name,
            price=0,            # you can decide price later
            specials=False,
            items=True,
            damage=False,
            heal=False,
            armor=False,
            amount=self.amount,
            rarity=50,
            manaCost=0,
            weapon=True
        )

    def attach(self, user):
        if user.weapon:
            user.items.append(user.weapon)
            print(f"{self.name} was placed into your inventory.")
        user.weapon = self
        user.damage += self.amount
        print(f"{self.name} equipped! Damage increased by {self.amount}.")

    def detach(self, user):
        print(f"{self.name} removed.")
        user.damage -= self.amount

        weaponItem = self.toStoreItem()

        freeSpace = user.space - len(user.items)
        if freeSpace > 0:
            user.items.append(weaponItem)
            print(f"{self.name} was placed into your inventory.")
        else:
            print("Inventory full! Armor dropped on the ground!")

        user.weapon = None

    
        