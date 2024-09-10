import pygame
from random import *

# assign colours and hardness
color_hardness = {
    1: (pygame.Color(242, 135, 5), 1),  # orange, hardness 1
    2: (pygame.Color(242, 199, 68), 1),    # yellow, hardness 1
    3: (pygame.Color(4, 216, 156), 2),      # green, hardness 2
    4: (pygame.Color(242, 61, 61), 2),      # red, hardness 2
    5: (pygame.Color(28, 147, 255), 3)       # blue, hardness 3
}
countCollision = [0 for x in range(0, 42)]

class Brick:
    x_position: int
    y_position: int
    color = None
    hardness: int
    brickCoordinates = []
    countIndex: int = 0

    def __init__(self):
        self.start_X = 35  # Starting X position for bricks
        self.start_Y = 37  # Starting Y position for bricks
        self.x_position: int
        self.y_position: int

        for i in range(3):  # Number of rows
            x_position = self.start_X  # Reset X position for each row
            y_position = self.start_Y + i * 52  # Calculate Y position for each row

            for j in range(14):  # Number of columns
                assignment = randint(1, 5)
                self.color, self.hardness = color_hardness[assignment] # assigns stuff according to hardness(dict)

                coordinates = (x_position, y_position, self.color, self.hardness, self.countIndex)
                self.brickCoordinates.append(coordinates)

                x_position += 53  # Move to the next column
                self.countIndex += 1

    def displayBrick(self , screen: pygame.Surface):
        for coord in self.brickCoordinates:  # Draw each brick
            pygame.draw.rect(screen, coord[2], (coord[0], coord[1], 50, 50), 0, 10)