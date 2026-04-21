import random
import time
import os
from audioMixer import SoundManager

sm = SoundManager()

class Horse:
    
    def __init__(self, name):
        self.name = name
        self.speed = random.randint(1, 10)

    

horse1 = Horse("Thomas the Great          |")
horse2 = Horse("Judie the Baddie          |")
horse3 = Horse("Billy the Silly Willy     |")
horse4 = Horse("Tracy the Tickle Monster  |")
horse5 = Horse("Conor                     |")
horse6 = Horse("Smith the Crip            |")
horse7 = Horse("Patrick the Second Coming |")
horse8 = Horse("Jack the Black            |")
horse9 = Horse("Steve the Man             |")
horse10 = Horse("Lauren the Loli Lover     |")

allHorse = [horse1, horse2, horse3, horse4, horse5, horse6, horse7, horse8, horse9, horse10]

def playableHorse():
    return random.sample(allHorse, 5)
    
    
def race(wallet, wager):
    sm.play_music("animeHorse")
    def play_ascii_video(folder_path, fps=30):
        #sm.play_music("animeHorse")
        # Get sorted list of text files
        frames = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])
        
        frame_duration = 1 / fps
        
        for frame_file in frames:
            with open(os.path.join(folder_path, frame_file), 'r') as f:
                # Clear the terminal screen
                print("\033[H\033[J", end="") 
                # Print the frame
                print(f.read())
                
            time.sleep(0.025)

    # Usage
    ascii_frames_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ascii_frames'))
    play_ascii_video(ascii_frames_path, fps=30)
    totalSpeed = 0
    winner = ""
    raceHorse = playableHorse()
    print("Horses in the race:")
    for count in range(len(raceHorse)):
        totalSpeed = totalSpeed + raceHorse[count].speed
    
    
    for count in range(len(raceHorse)):
        print(f"{count}. {raceHorse[count].name} chances: {round(float(raceHorse[count].speed / totalSpeed) * 100, 2)}% ")
      
    try:
        playerChoice = int(input("Which horse would you like to bet on (0-4)?\n> "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return 0
    
    # Simulate the race
    positions = [0] * len(raceHorse)
    finish_line = 100
    while max(positions) < finish_line:
        for i in range(len(raceHorse)):
            positions[i] += random.randint(1, raceHorse[i].speed)
        # Print progress
        for i in range(len(raceHorse)):
            progress = min(positions[i] // 2, 50)  # Cap at 50 dashes for display
            print(f"{raceHorse[i].name}: {'-' * progress}")
        print()  # New line
        time.sleep(0.5)  # Slow down for visibility
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # Determine winner
    winner_index = positions.index(max(positions))
    winner = raceHorse[winner_index]
    print(f"The winner is {winner.name}!")
    
    
    if playerChoice == winner_index:
        print("You win!!!")
        sm.fadeout_music(1000)
        print(int((wager * (1.0 + (1.0 - (winner.speed / totalSpeed))))))
        return wallet + int((wager * (1.0 + (1.0 - (winner.speed / totalSpeed)))))
    else:
        print("You lose!")
        sm.fadeout_music(1000)
        return wallet - wager
    
    
        
        
        
    
        
    
         
    
    