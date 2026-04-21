class Armor:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount   # amount = defense bonus
        self.durability = 100
        self.armor = True
        self.weapon = False
        
    def toStoreItem(self):
        from classes.items import StoreItems 
        return StoreItems(
            self.name,
            price=0,       
            specials=False,
            items=True,
            damage=False,
            heal=False,
            armor=True,
            amount=self.amount,
            rarity=50,
            manaCost=0,
            durability= self.durability
        )
        
    def attach(self, user):
        if user.armor:
            print(f"Removing old armor: {user.armor.name}")

        user.armor = self
        user.defense += self.amount
        print(f"{self.name} equipped! Defense increased by {self.amount}.")
        

    def detach(self, user):
        print(f"{self.name} removed.")
        user.defense -= self.amount

        armorItem = self.toStoreItem()

        freeSpace = user.space - len(user.items)
        if freeSpace > 0:
            user.items.append(armorItem)
            print(f"{self.name} was placed into your inventory.")
        else:
            print("Inventory full! Armor dropped on the ground!")

        user.armor = None
        
    def repairCost(self):
        """Formula for repair cost."""
        missing = 100 - self.durability
        return missing * 2  # 2 coins per durability point (change as needed)

    def repair(self):
        """Repair to full durability."""
        self.durability = 100


    
        