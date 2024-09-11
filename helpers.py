from Ball import Ball
from strikingPad import Pad
from Brick import Brick
import pygame
import sys

# Function to display the 'Main Menu'
def main_menu(background_image_path):
    # Load the background image using the provided path
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.smoothscale(background_image, (Screen_Width, Screen_Height))

    # Button dimensions and colors
    button_width = 200
    button_height = 50
    button_color = (255, 22, 15) 
    button_hover_color = (254, 147, 36)
    small_font = pygame.font.Font(None, 24)  # Smaller font for menu options

    # Sound toggle state (True = On, False = Off)
    is_sound_on = True

    while True:
        Screen.blit(background_image, (0, 0))
        # Start Game button
        start_button_rect = pygame.Rect(20, 20 , button_width, button_height)
        start_text = small_font.render("Start Game", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button_rect.center)


        # Sound toggle button
        sound_text = "Sound: On" if is_sound_on else "Sound: Off"
        sound_button_rect = pygame.Rect(20, 40 + button_height , button_width, button_height)
        sound_text_surface = small_font.render(sound_text, True, (255, 255, 255))
        sound_text_rect = sound_text_surface.get_rect(center=sound_button_rect.center)

        # Quit Game button
        quit_button_rect = pygame.Rect(20, 110 + button_height, button_width, button_height)
        quit_text = small_font.render("Quit Game", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)


        # Button hover effects
        mouse_pos = pygame.mouse.get_pos()
        for button_rect, button_text_rect in [
            (start_button_rect, start_text_rect),
            (quit_button_rect, quit_text_rect),
            (sound_button_rect, sound_text_rect)]:

            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(Screen, button_hover_color, button_rect)
            else:
                pygame.draw.rect(Screen, button_color, button_rect)

        Screen.blit(start_text, start_text_rect)#Draw texts
        Screen.blit(quit_text, quit_text_rect)
        Screen.blit(sound_text_surface, sound_text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if start_button_rect.collidepoint(mouse_pos): 
                    return True # Start the game
                elif sound_button_rect.collidepoint(mouse_pos):
                    is_sound_on = not is_sound_on  # Toggle sound state
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                    
def display_game_over(Game_OV):
    # Button variables
    but_width = 200
    but_height = 50
    button_color = (200, 200, 200)  # Light Gray
    button_hover_color = (255, 69, 0)  # Bright Red


    
    # Load Game Over background
    game_ov_bg = pygame.image.load(Game_OV)
    game_ov_bg = pygame.transform.smoothscale(game_ov_bg, (Screen_Width, Screen_Height))
    
    small_font = pygame.font.Font(None, 24)
    
    waiting = True
    while waiting:
        Screen.blit(game_ov_bg, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        score_message = small_text.render(f"Your score: {Score}", True, (255, 255, 255))
        score_rect = score_message.get_rect(center=(Screen_Width // 2, Screen_Height // 2 - 100))
        Screen.blit(score_message, score_rect)

        button_gap = 20  
        bottom_padding = 50 

        # Main Menu button
        Main_menu_but = pygame.Rect((Screen_Width // 2 - but_width // 2,Screen_Height - but_height - bottom_padding - button_gap, but_width, but_height))
        main_menu_text = small_font.render("Main Menu", True, (255, 255, 255))
        main_menu_text_rect = main_menu_text.get_rect(center=Main_menu_but.center)

        # Restart button 
        Restart_button = pygame.Rect((Screen_Width // 2 - but_width // 2,Screen_Height - 2 * (but_height + button_gap) - bottom_padding, but_width,but_height))
        restart_surface = small_font.render("Restart", True, (255, 255, 255))
        restart_text_rect = restart_surface.get_rect(center=Restart_button.center)

        #Effects
        for button_rect, button_text, button_text_rect in [
            (Main_menu_but, main_menu_text, main_menu_text_rect),
            (Restart_button, restart_surface, restart_text_rect)]:
            
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(Screen, button_hover_color, button_rect)
            else:
                pygame.draw.rect(Screen, button_color, button_rect)

            Screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if Main_menu_but.collidepoint(mouse_pos):
                    return False  # Go to Main Menu
                elif Restart_button.collidepoint(mouse_pos):
                    return True # Restart the game
                
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
    Brick_collision = False
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
            Brick_collision = True
            break  # Exit loop after handling one collision

    if(Brick_collision)and not (Brick_Destroy):
        return (False,True,False,False)
    elif(Brick_Destroy):
        return (False,False,True,False)# If brick destroy
   
    if ball.y + ball.y_velocity > Screen_Height - ball.radius:
        Floor_collision = True
    if  Floor_collision:
        return (False,False,False,True)
    
    return (False,False,False,False) # No collision
#Level_up,Increase Speed and make bricks More harder
def level_up():
    global Level, ball, Bricks,Speed
    Level += 1
    Speed += 3  # Increase pad speed
    ball.reset(Ball_X,Ball_Y)
    ball.increase_speed(2)  # Increase ball speed by 2 units
    pad.reset(Screen_Width,Screen_Height,Pad_Width,Pad_Height)



