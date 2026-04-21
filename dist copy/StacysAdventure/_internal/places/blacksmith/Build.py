from classes.items import StoreItems, CraftItems
from classes.player.createPlayer import Player


craftableItems = [
    CraftItems("Reptillian Origami Sweater", 100, False, True, False, False, True, 25, 10, 0, {"scales": 3}),
    CraftItems("Wooden Gun", 40, False, False, True, False, False, 9, 70, 0, {"logs": 3 }),
    CraftItems("UwU Hydration Hot Pot", 60, False, True, False, True, False, 100, 10, 0, {"Top Ramen": 2, "Gamer Girl Bath Water": 1})
    
    
]


def build(player, chosenItem):
    needed = chosenItem.required_items   # example: {"logs": 4}

    # SAFELY count only valid items
    inv_count = {}

    for item in player.items:
        # Skip invalid entries (strings or None)
        if not hasattr(item, "name"):
            continue  

        inv_count[item.name] = inv_count.get(item.name, 0) + 1

    # Check materials
    for material, amt in needed.items():
        have = inv_count.get(material, 0)
        if have < amt:
            print(f"Missing {material}: need {amt}, have {have}")
            return None


    # Remove materials by name
    for material, amt in needed.items():
        removed = 0
        
        for item in list(player.items):  # iterate over a copy
            if hasattr(item, "name") and item.name == material:
                player.items.remove(item)
                removed += 1
                if removed == amt:
                    break

    # Add crafted product
    player.quickStorage(chosenItem)
    print(f" Successfully crafted {chosenItem.name}!")
    return chosenItem

