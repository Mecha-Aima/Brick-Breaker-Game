from Ball import Ball
from strikingPad import Pad
from Brick import Brick
import pygame
import sys

# Main Menu
def main_menu(background_image_path, Screen, Screen_Width, Screen_Height):
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


        mouse_pos = pygame.mouse.get_pos()
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

def display_game_over(Screen):
    font = pygame.font.Font(None, 72)  # Set the font and size
    game_over_message = font.render("GAME OVER", True, (255, 10, 10))  
    text_rect = game_over_message.get_rect(center=(Screen_Width // 2, Screen_Height // 2))
    Screen.blit(game_over_message, text_rect)

    # Score message
    score_message = small_text.render(f"Your score: {Score}", True, (255, 255, 255))
    score_rect = score_message.get_rect(center=(Screen_Width // 2, Screen_Height // 2 + 50))
    Screen.blit(score_message, score_rect)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                 waiting = False 

