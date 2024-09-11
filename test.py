import pygame
from Game import Game

def main():
    # Initialize game parameters
    level = 1  # Starting level
    score = 0  # Initial score
    game_won = False;

    # Create a Game instance
    game = Game(level, score)
    game.main_menu()

    while not game_won:
        result = game.run()
        if result == 'level_complete':
            level += 1
            if level == 4:
                game_won = True
            elif level == 3:
                game.lives = 2
            else:
                game.lives = 3
            # Check win
            if game_won:
                play_again = game.display_you_won()
                if play_again == "play_again":
                    level = 1
                    score = 0
                    game = Game(level, score)
                    game_won = False

        elif result == "restart":
                # Reset the game
                level = 1
                score = 0
                game = Game(level, score)
        
    

if __name__ == "__main__":
    main()
