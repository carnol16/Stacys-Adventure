# Stacy's Adventure

A terminal-based RPG where you help Stacy — a towering goth girl from the pastel suburb of Lollipop Circle — recruit a hero and fight off a ridiculous cast of villains threatening her most prized possession.

## About

Stacy's Adventure is a fully playable Python RPG built in the terminal. It features turn-based combat, character creation, a progression system with boss fights, multiple shops to spend your gold, and a global leaderboard to track how far you made it.

The game has animated typewriter-style dialogue, dynamic battle music, and colored text output to give it personality beyond a standard CLI game.

## Features

- **Character Creation** — choose your name, class (Warrior, Basement Dweller, Boat Man, Ninja, or whatever you want), and favorite color
- **Turn-Based Combat** — fight randomized enemies with attacks, specials, and mana management
- **Boss Fights** — every 5 enemies you face a boss with scaled health
- **Shops between fights:**
  - Blacksmith — upgrade your weapon and armor
  - Store — buy consumables (online/offline mode supported)
  - Restaurant — restore health
  - Casino — gamble your gold
- **Leaderboard** — tracks your fight number, character name, class, and date
- **Threaded Battle Music** — randomized audio that plays in the background during combat
- **Save System** — player state is saved between sessions

## Setup

```bash
# Clone the repo
git clone https://github.com/carnol16/StacysAdventure.git
cd StacysAdventure

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


# Run the game
python main.py
```

> **Note:** When prompted for online features, choose `y` if you want live leaderboard support or `n` to play offline.

## Requirements

- Python 3.10+
- pygame
- colorama
- requests

## Project Structure

```
StacysAdventure/
├── main.py               # Entry point and game loop
├── gameplay/
│   └── gameplay.py       # Core game logic, combat, shop routing
├── classes/
│   ├── enemy.py          # Enemy and Boss classes
│   ├── items.py          # Item definitions
│   ├── save.py           # Save/load system
│   └── player/           # Player class, weapons, armor, specials
├── places/
│   ├── blacksmith/       # Weapon/armor upgrades
│   ├── casino/           # Gambling minigame
│   ├── restaurant/       # Health restoration
│   └── store/            # Item shop (online + offline versions)
├── audio/                # Battle music clips
├── audioMixer.py         # Sound management with pygame
└── leaderboard.json      # Local leaderboard data
```

## Built With

- **Python** — core game logic
- **pygame** — audio playback
- **colorama** — colored terminal output
- **requests** — online store and leaderboard features
