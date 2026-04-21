class SaveState:
    
    def saveGame(mainCharacter):
        
        data = {
            "type": mainCharacter.type,
            "color": mainCharacter.color,
            "name": mainCharacter.name,
            "mana": mainCharacter.mana,
            "space": mainCharacter.space,
            "items": mainCharacter.items,
            "wallet": mainCharacter.wallet,
            "weapon": mainCharacter.weapon,
            "armor": mainCharacter.armor,
            "badBoy": mainCharacter.badBoy,
            "increaseDefend": mainCharacter.increaseDefend,
            "partyMembers": mainCharacter.partyMembers,
            "activeParty": mainCharacter.activeParty
        }
        