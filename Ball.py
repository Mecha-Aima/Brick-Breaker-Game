import pygame

# return (pad,boundary,bricks)
def check_collision(ball: Ball, pad: Pad, brick: Brick) -> tuple:

    # Check collision with the pad and reverse ball if necessary
    tempPad = pygame.Rect(pad.x, pad.y, pad.padWidth, pad.padHeight)
    pad_collision = ball.circle_rectangle_collision(tempPad)
    
    if pad_collision:
        ball.reverse_y()
        return (True,False,False) # ball can only collide with 1 surface at a time

    # Check collision with screen boundaries
    boundary_collision = (
        ball.x - ball.radius <= 0 or  # Left boundary
        ball.x + ball.radius >= ball.screen_width or  # Right boundary
        ball.y - ball.radius <= 0 or  # Top boundary
        ball.y + ball.radius >= ball.screen_height  # Bottom boundary
    )

    if(boundary_collision):
        return (False,True,False)
    
    # Check collision with the bricks, reverse speed & check no. col
    Brick_collition = False
    for collision in brick.brickCoordinates:
        tempBrick = pygame.Rect((collision[0], collision[1], 50, 50))

        if ball.circle_rectangle_collision(tempBrick):
            brickIndex = collision[4]  # Get the index of the brick
            countCollision[brickIndex] += 1  # Increment collision count

            # Check if the brick's hardness limit is reached
            if countCollision[brickIndex] >= collision[3]:
                brick.brickCoordinates.remove(collision)  # Remove the brick
            # Reverse speed upon collision
            ball.reverse_x()
            ball.reverse_y()
            Brick_collition = True
            break  # Exit loop after handling one collision

    if(Brick_collition):
        return (False,False,True)
    
    return (False,False,False) # no collition
 

class Ball:
    def __init__(self, radius : int, img : str, x : int, y : int, screen_width : int, screen_height : int, x_velocity : int, y_velocity : int) -> None:
        self.radius = radius  # ball radius

        # load the image for ball and setting it
        self.image = pygame.transform.scale(pygame.image.load(img), (radius * 2, radius * 2)) # loading ball image and set width and height whicj is a new surface
        self.mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA) # create the mask which is also a surface, SRCAlPHA add transparency on selected pixels
        pygame.draw.circle(self.mask, (255, 255, 255), (radius, radius), radius) # draw the circle inside mask surface
        self.image.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGB_MIN) # blit function draw one surface over another surface, pygame.BLEND_RGB_MIN means it add tranparency only outside the ball

        self.x = x  # initial x-coordinate
        self.y = y  # initial y-coordinate

        self.screen_width = screen_width  # width of the game window
        self.screen_height = screen_height  # height of the game window

        self.x_velocity = x_velocity  # velocity along the x-axis in pixels
        self.y_velocity = y_velocity  # velocity along the y-axis in pixels

    def reverse_x(self) -> None:
        self.x_velocity = -self.x_velocity  # Reverse the x-velocity to bounce back
    
    def reverse_y(self) -> None:
        self.y_velocity = -self.y_velocity  # Reverse the y-velocity to bounce back

    def move(self) -> None:
        # update ball's x-coordinate based on x_velocity
        self.x += self.x_velocity

        # check for collision with left or right walls
        if self.x <= self.radius:  # ball hits the left wall
            self.x = self.radius
            self.reverse_x()

        elif self.x + self.radius >= self.screen_width:  # ball hits the right wall
            self.x = self.screen_width - self.radius
            self.reverse_x()
        
        # update ball's y-coordinate based on y_velocity
        self.y += self.y_velocity

        # check for collision with top or bottom walls
        if self.y <= self.radius:  # ball hits the top wall
            self.y = self.radius
            self.reverse_y()
            
        elif self.y + self.radius >= self.screen_height:  # ball hits the bottom wall
            self.y = self.screen_height - self.radius
            self.reverse_y()

    def draw(self, screen : pygame.Surface) -> None:
        # draw ball image surface over the window
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

    def circle_rectangle_collision(self, rect):
        cx, cy = self.x, self.y
        rx, ry, rw, rh = rect

        # Find the closest point on the rectangle to the circle's center
        closest_x = max(rx, min(cx, rx + rw))
        closest_y = max(ry, min(cy, ry + rh))

        # Calculate the distance between the circle's center and the closest point
        distance_x = cx - closest_x
        distance_y = cy - closest_y
        distance_squared = distance_x ** 2 + distance_y ** 2

        return distance_squared <= self.radius ** 2