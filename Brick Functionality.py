
import pygame
from pygame import *
from random import *
pygame.init()

red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
pink = pygame.Color(255, 192, 203)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
countCollision = [0 for x in range(0, 42)]


"""
This function aims to detect the collision of the ball and remove the brick at the moment if hardness count of the brick
is completed
"""
def collisionDetection(ball,bricks, countCollision):
    for collision in bricks.brickCoordinates:
        tempBrick = pygame.Rect((collision[0], collision[1], 50, 50))
        if ball.circle_rectangle_collision((ball.ballX, ball.ballY), ball.ballRadius, tempBrick):
            brickIndex = collision[4]  # Get the index of the brick
            countCollision[brickIndex] += 1  # Increment collision count

            # Check if the brick's hardness limit is reached
            if countCollision[brickIndex] >= collision[3]:
                bricks.brickCoordinates.remove(collision)  # Remove the brick

            # Reverse speed upon collision
            ball.speedX = -(randint(1,3))
            ball.speedY = +(randint(1,3))
            break  # Exit loop after handling one collision

    return ball.speedX, ball.speedY

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Brick Breaker Game")

# Load and scale the images
image = pygame.image.load("C:\\Users\\Star\\Downloads\\wood.jfif")
bgImage = pygame.image.load("C:\\Users\\Star\\Downloads\\background image.jfif")
image = pygame.transform.scale(image, (50, 50))  # Scale image to fit brick size
bgImage = pygame.transform.scale(bgImage, (800, 600))


class Ball:
    def __init__(self):
        self.ballRadius: int = 10
        self.ballX: int = 400
        self.ballY: int = 500
        self.speedX: int = 2
        self.speedY: int = -2

    def drawAndMoveBall(self):
        # Draw the ball
        draw.circle(screen, red, (self.ballX, self.ballY), self.ballRadius)
        # Move the ball
        self.ballY += self.speedY
        self.ballX += self.speedX

        # Check wall collisions
        if self.ballY <= 0:
            self.speedY = 3
        elif self.ballY >= 550:             #This is the border ground condition but we want to lost the ball at ground
            self.speedY = -3                #meeting so we can remove this condition for propoer life counting
        if self.ballX >= 800:
            self.speedX = -3
        elif self.ballX <= 0:
            self.speedX = 3

    @staticmethod
    def circle_rectangle_collision(circle_pos, circle_radius, rect):
        cx, cy = circle_pos
        rx, ry, rw, rh = rect

        # Find the closest point on the rectangle to the circle's center
        closest_x = max(rx, min(cx, rx + rw))
        closest_y = max(ry, min(cy, ry + rh))

        # Calculate the distance between the circle's center and the closest point
        distance_x = cx - closest_x
        distance_y = cy - closest_y
        distance_squared = distance_x ** 2 + distance_y ** 2

        return distance_squared <= circle_radius ** 2

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
                if assignment == 1:
                    self.color = pink
                    self.hardness = 1
                elif assignment == 2:
                    self.color = yellow
                    self.hardness = 1
                elif assignment == 3:
                    self.color = green
                    self.hardness = 2
                elif assignment == 4:
                    self.color = red
                    self.hardness = 2
                elif assignment == 5:
                    self.color = blue
                    self.hardness = 3
                coordinates = (x_position, y_position, self.color, self.hardness, self.countIndex)
                self.brickCoordinates.append(coordinates)
                x_position += 53  # Move to the next column
                self.countIndex += 1

    def displayBrick(self):
        for coord in self.brickCoordinates:  # Number of columns
            pygame.draw.rect(screen, coord[2], (coord[0], coord[1], 50, 50), 0, 10)


# Create an instance of Brick
bricks = Brick()
ball = Ball()
# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Fill the screen with the background image
    screen.blit(bgImage, (0, 0))

    # Draw the bricks
    bricks.displayBrick()

    ball.drawAndMoveBall()

    # Check brick collisions
    ball.speedX, ball.speedY = collisionDetection(ball,bricks, countCollision)

    clock.tick(200)
    # Update the display
    pygame.display.update()

