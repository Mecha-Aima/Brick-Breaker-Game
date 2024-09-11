import pygame
import numpy as np
from random import *

# assign colours and hardness
color_hardness = {
    1: (pygame.Color(242, 135, 5), 1),  # orange, hardness 1
    2: (pygame.Color(242, 199, 68), 1),    # yellow, hardness 1
    3: (pygame.Color(4, 216, 156), 2),      # green, hardness 2
    4: (pygame.Color(242, 61, 61), 2),      # red, hardness 2
    5: (pygame.Color(28, 147, 255), 3)       # blue, hardness 3
}

# Define probability distributions for different levels
level_probabilities = {
    1: np.array([0.2, 0.3, 0.2, 0.2, 0.1]),  # Level 1 probabilities
    2: np.array([0.1, 0.1, 0.3, 0.3, 0.2]),  # Level 2 probabilities
    3: np.array([0.1, 0.1, 0.2, 0.2, 0.4])  # Level 3 probabilities
}

level_brick_counts = {
    1: 28,  # Level 1: 42 bricks
    2: 42,  # Level 2: 56 bricks
    3: 56  # Level 3: 70 bricks
}

class Brick:
    x_position: int
    y_position: int
    color = None
    hardness: int
    brickCoordinates = []
    countIndex: int = 0

    def __init__(self, level):
        self.start_X = 35  # Starting X position for bricks
        self.start_Y = 37  # Starting Y position for bricks
        self.x_position: int
        self.y_position: int
        probabilities = level_probabilities[level]

        num_rows, num_col = 3, 14
        if level in level_brick_counts:
            num_rows, num_col = level_brick_counts[level] // 14, 14
        self.brickCoordinates.clear()#Clear Brick Coordinates
        for i in range(num_rows):  # Number of rows
            x_position = self.start_X  # Reset X position for each row
            y_position = self.start_Y + i * 52  # Calculate Y position for each row

            for j in range(num_col):  # Number of columns
                # Select a random color based on probabilities
                assignment = np.random.choice(list(color_hardness.keys()), p=probabilities)
                self.color, self.hardness = color_hardness[assignment] # assigns stuff according to hardness(dict)

                coordinates = (x_position, y_position, self.color, self.hardness, self.countIndex)
                self.brickCoordinates.append(coordinates)

                x_position += 53  # Move to the next column
                self.countIndex += 1

    def displayBrick(self , screen: pygame.Surface):
        for coord in self.brickCoordinates:  # Draw each brick
            pygame.draw.rect(screen, coord[2], (coord[0], coord[1], 50, 50), 0, 10)
