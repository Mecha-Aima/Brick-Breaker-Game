import pygame
from Game import Game
import sys

def main():
    # Initialize game parameters
    level = 1  # Starting level
    score = 0  # Initial score
    game_won = False;

    # Read previous highscore
    with open('highscore.txt', 'r') as f:
        highscore = f.read()
        if highscore == "":
            highscore = 0
        else:
            highscore = int(highscore)

    # Create a Game instance
    game = Game(level, score, highscore)
    game.main_menu()

    while not game_won:
        result = game.run()

        # Update highscore
        if game.score > highscore:
            highscore = game.score
            f = open('highscore.txt', 'w')
            f.write(str(highscore))
            f.close()

        # Check if game is won
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
        elif result == "exit":
            pygame.quit()
            sys.exit()
    
if __name__ == "__main__":
    main()
