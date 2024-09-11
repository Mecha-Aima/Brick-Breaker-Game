import pygame
from Game import Game

def main():
    # Initialize game parameters
    level = 1  # Starting level
    score = 0  # Initial score
    game_won = False;

    # Create a Game instance
    game = Game(level, score)

    while not game_won:
        result = game.run()
        if result == 'level_complete':
            level += 1
            if level == 4:
                game_won = True
                break
            elif level == 3:
                game.lives = 2
            else:
                game.lives = 3

        elif result == "restart":
                # Reset the game
                level = 1
                score = 0
                game = Game(level, score)
        
    if game_won:
        print("You won the game!")
    else:
        print("You lost the game!")

if __name__ == "__main__":
    main()
