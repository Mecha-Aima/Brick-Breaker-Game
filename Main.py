from Ball import Ball
from striking_pad import Pad
from bricks import Brick
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
Screen_Width = 800
Screen_Height = 600
# Create the screen object
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))
# Set the title of the window
pygame.display.set_caption("Brick Breaker")
# Set the frame rate
Clock = pygame.time.Clock()

# Load Assets
Hit_Sound = pygame.mixer.Sound("Assets/Hit.wav")
Break_Sound = pygame.mixer.Sound("Assets/Break.wav")
Paddle_Hit=pygame.mixer.Sound("Assets/Paddle_hit.wav")
Game_OV_Sound=pygame.mixer.Sound("Assets/Game_lost.mp3")
evil_sound=pygame.mixer.Sound("Assets/evil.mp3")
Win_sound=pygame.mixer.Sound("Assets/Win.wav")
Background = pygame.image.load("Assets/back.jpg").convert()
Background = pygame.transform.smoothscale(Background, (Screen_Width, Screen_Height))
Pad_sprite="Assets/paddle.png"
Ball_Sprite="Assets/ball.png"
Brick_img="Assets/wood.jpg"
life_image = pygame.image.load("Assets/life.png")
life_image = pygame.transform.smoothscale(life_image, (40, 40))  # Resize to 40x40 pixels (or adjust as needed)
life_rect = life_image.get_rect()
life_x = 10   # 10 pixels padding from the right
life_y =  Screen_Height - life_rect.height - 30# 10 pixels padding from the bottom


# Defining Variables
Lives=3
Level=1
Speed=10
Score=0
High_score=0
Ball_Radius = 15
Ball_X = Screen_Width // 2 
Ball_Y = Screen_Height // 2  
Ball_X_Velocity = 7
Ball_Y_Velocity = 7
Pad_Width=100
Pad_Height=15
Collsion_Check=()
Game_Over = False
Game_Start = False  
play_sound=False
countCollision= [0 for x in range(0, 42)]


#Collision 
# return (pad,boundary/Bricks,Brick-Destroy,floor)
def check_collision(ball: Ball, pad: Pad, brick: Brick) -> tuple:

    # Check collision with the pad and reverse ball if necessary
    tempPad = pygame.Rect(pad.x, pad.y, pad.padWidth, pad.padHeight)
    pad_collision = ball.circle_rectangle_collision(tempPad)
    
    if pad_collision:
        ball.reverse_y()
        return (True,False,False,False) # Ball can only collide with 1 surface at a time

    # Check collision with screen boundaries
    boundary_collision = (
        ball.x - ball.radius <= 0 or  # Left boundary
        ball.x + ball.radius >= ball.screen_width or  # Right boundary
        ball.y - ball.radius <= 0 or  # Top boundary
        ball.y + ball.radius >= ball.screen_height  # Bottom boundary
    )

    if(boundary_collision):
        return (False,True,False,False)
    
    # Check collision with the bricks, reverse speed & check no. col
    Brick_collition = False
    Brick_Destroy=False
    Floor_collision=False
    for collision in brick.brickCoordinates:
        tempBrick = pygame.Rect((collision[0], collision[1], 50, 50))

        if ball.circle_rectangle_collision(tempBrick):
            brickIndex = collision[4]  # Get the index of the brick
            countCollision[brickIndex] += 1  # Increment collision count

            # Check if the brick's hardness limit is reached
            if countCollision[brickIndex] >= collision[3]:
                brick.brickCoordinates.remove(collision)  # Remove the brick
                Brick_Destroy=True
            # Reverse speed upon collision
            ball.reverse_y()
            Brick_collition = True
            break  # Exit loop after handling one collision

    if(Brick_collition)and not (Brick_Destroy):
        return (False,True,False,False)
    elif(Brick_Destroy):
        return (False,False,True,False)# If brick destroy
   
    if ball.y>=Screen_Height-20:
        Floor_collision=True
        ball.x=Ball_X
        ball.y=Ball_Y
        pad.x=(Screen_Width-Pad_Width)//2
        pad.y=Screen_Height-Pad_Height-50
    if  Floor_collision:
        return (False,False,False,True)
    
    return (False,False,False,False) # No collition


# Create a Ball object
ball = Ball(
    Ball_Radius,
    Ball_Sprite,
    Ball_X,
    Ball_Y,
    Screen_Width,
    Screen_Height,
    Ball_X_Velocity,
    Ball_Y_Velocity,
)
#Create a Pad
pad = Pad(Pad_sprite,Screen_Width,Screen_Height,Pad_Width,Pad_Height)

#Create Bricks
Bricks=Brick()

# Main game loop
while not Game_Over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game_Over = True
    # Taking Input
    Key_press = pygame.key.get_pressed()
    if Key_press[pygame.K_SPACE]:
        Game_Start = True
    if Key_press[pygame.K_LEFT]and Game_Start:
        pad.move(-Speed)
    if Key_press[pygame.K_RIGHT]and Game_Start:
        pad.move(Speed)
    if Key_press[pygame.K_BACKSPACE]:
        print(countCollision)
    # Move the ball
    if Game_Start:
        ball.move()
    #Check collision n Play Sound
    Collsion_Check=check_collision(ball,pad,Bricks)
    if Collsion_Check[0]==1:
        Paddle_Hit.play()
    elif Collsion_Check[1]==1:
        Hit_Sound.play()
    elif Collsion_Check[2]==1:
        Break_Sound.play()

    elif Collsion_Check[3]==1:
        Game_OV_Sound.play()
        Lives-=1
        Game_Start=False
    
    #Game_Over
    if Lives==0:
        Game_Over=True
    #Check win
    if not 0 in countCollision:
        Win_sound.play()
        Level+=1
    #Draw the Background
    Screen.blit(Background, (0, 0))
    # Draw the ball
    ball.draw(Screen)
    #Draw the pad
    pad.draw(Screen)
    #Display Bricks
    Bricks.displayBrick(Screen)
    #Draw lives
    for i in range(Lives):
        Screen.blit(life_image, (life_x, life_y))
        life_x+=30
    life_x=10
    Clock.tick(60)
    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()
