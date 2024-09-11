import pygame
import sys
from Ball import Ball
from strikingPad import Pad
from Brick import Brick

class Game:
    def __init__(self, level, score, highscore=0):
       # Initialize the game with level and score as arguments
        self.level = level
        self.score = score
        self.highscore = highscore
        self.lives = 3 if level < 3 else 3  # Default starting lives
        self.speed = 12  # Default pad speed
        self.game_over = False
        self.game_start = False
        self.screen_width = 800
        self.screen_height = 600
        self.setup_pygame()
        self.load_assets()

        self.Ball_Radius = 15
        self.Ball_X = self.screen_width // 2 
        self.Ball_Y = self.screen_height // 2  
        self.Ball_X_Velocity = 7
        self.Ball_Y_Velocity = 7
        self.Pad_Width=100
        self.Pad_Height=15
        self.Collsion_Check=()
        self.life_rect = self.life_image.get_rect()
        self.life_x = 10   # 10 pixels padding from the right
        self.life_y =  self.screen_height - self.life_rect.height - 30# 10 pixels padding from the bottom

        # Create objects
        self.create_objects()

    def create_objects(self):
        self.ball = Ball(self.Ball_Radius, self.Ball_Sprite, self.Ball_X, self.Ball_Y, self.screen_width, self.screen_height, self.Ball_X_Velocity, self.Ball_Y_Velocity)
        self.pad = Pad(self.Pad_sprite, self.screen_width, self.screen_height, self.Pad_Width, self.Pad_Height)
        self.bricks = Brick(self.level)
        self.countCollision= [0 for _ in range(0, (self.level + 2)*14)]

    def setup_pygame(self):
        # Set up Pygame screen, caption, clock, etc.
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.small_text = pygame.font.Font(None, 24)
        self.is_sound_on = True
    
    def load_assets(self):
        """Load all assets like sounds and images."""
        self.Hit_Sound = pygame.mixer.Sound("Assets/Hit.wav")
        self.Break_Sound = pygame.mixer.Sound("Assets/Break.wav")
        self.Paddle_Hit = pygame.mixer.Sound("Assets/Paddle_hit.wav")
        self.Game_OV_Sound = pygame.mixer.Sound("Assets/Game_lost.mp3")
        self.evil_sound = pygame.mixer.Sound("Assets/evil.mp3")
        self.Win_sound = pygame.mixer.Sound("Assets/Win.wav")
        self.Background = pygame.image.load("Assets/back.jpg").convert()
        self.Game_OV_BG="Assets/Game_ov.jpg"
        self.Background = pygame.transform.smoothscale(self.Background, (self.screen_width, self.screen_height))
        self.life_image = pygame.image.load("Assets/life.png")
        self.life_image = pygame.transform.smoothscale(self.life_image, (40, 40)) 
        self.Pad_sprite = "Assets/paddle.png"
        self.Ball_Sprite="Assets/ball.png"
        self.Brick_img="Assets/wood.jpg"
        self.Menu_background="Assets/menu-bg.png"
        self.Lost_life_sound=pygame.mixer.Sound("Assets/Lost_life.wav")
        pygame.mixer.music.load("Assets/Main_sound.wav")

    def main_menu(self):
        # Load the background image using the provided path
        background_image = pygame.image.load(self.Menu_background).convert()
        background_image = pygame.transform.smoothscale(background_image, (self.screen_width, self.screen_width))

        # Button dimensions and colors
        button_width = 200
        button_height = 50
        button_color = (255, 22, 15) 
        button_hover_color = (254, 147, 36)
        small_font = pygame.font.Font(None, 24)  # Smaller font for menu options

        # Sound toggle state (True = On, False = Off)
        if self.is_sound_on:
            print("Playing music")
            pygame.mixer.music.play(loops=-1)

        while True:
            self.screen.blit(background_image, (0, 0))
            # Start Game button
            start_button_rect = pygame.Rect(20, 20, button_width, button_height)
            start_text = small_font.render("Start Game", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=start_button_rect.center)


            # Sound toggle button
            sound_text = "Sound: On" if self.is_sound_on else "Sound: Off"
            sound_button_rect = pygame.Rect(20, 40 + button_height, button_width, button_height)
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
                    pygame.draw.rect(self.screen, button_hover_color, button_rect)
                else:
                    pygame.draw.rect(self.screen, button_color, button_rect)

            self.screen.blit(start_text, start_text_rect)   #Draw texts
            self.screen.blit(quit_text, quit_text_rect)
            self.screen.blit(sound_text_surface, sound_text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    if start_button_rect.collidepoint(mouse_pos): 
                        return True # Start the game
                    elif sound_button_rect.collidepoint(mouse_pos):
                        self.is_sound_on = not self.is_sound_on  # Toggle sound state
                        if self.is_sound_on:
                            pygame.mixer.music.play(loops=-1)
                        else:
                            pygame.mixer.music.stop()
                    elif quit_button_rect.collidepoint(mouse_pos):
                        return False
    

    def display_game_over(self, Game_OV):
    # Button variables
        but_width = 200
        but_height = 50
        button_color = (200, 200, 200)  # Light Gray
        button_hover_color = (255, 69, 0)  # Bright Red
        pygame.mixer.music.stop()
        
        # Load Game Over background
        game_ov_bg = pygame.image.load(Game_OV)
        game_ov_bg = pygame.transform.smoothscale(game_ov_bg, (self.screen_width, self.screen_height))
        
        small_font = pygame.font.Font(None, 24)
        
        waiting = True
        while waiting:
            self.screen.blit(game_ov_bg, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            # Check for new highscore
            if self.score > self.highscore:
                highscore_message = small_font.render("New Highscore!", True, (144, 238, 144))  # Soft green color for highscore
                highscore_rect = highscore_message.get_rect(center=(self.screen_width // 2, 50))  # Centered with y-offset of 50px
                self.screen.blit(highscore_message, highscore_rect)
                
            score_message = self.small_text.render(f"Your score: {self.score}", True, (255, 255, 255))
            score_rect = score_message.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 200))
            self.screen.blit(score_message, score_rect)

            button_gap = 20  
            bottom_padding = 50 

            # Main Menu button
            Main_menu_but = pygame.Rect((self.screen_width // 2 - but_width // 2, self.screen_height - but_height - bottom_padding - button_gap, but_width, but_height))
            main_menu_text = small_font.render("Main Menu", True, (255, 255, 255))
            main_menu_text_rect = main_menu_text.get_rect(center=Main_menu_but.center)

            # Restart button 
            Restart_button = pygame.Rect((self.screen_width // 2 - but_width // 2, self.screen_height - 2 * (but_height + button_gap) - bottom_padding, but_width,but_height))
            restart_surface = small_font.render("Restart", True, (255, 255, 255))
            restart_text_rect = restart_surface.get_rect(center=Restart_button.center)

            #Effects
            for button_rect, button_text, button_text_rect in [
                (Main_menu_but, main_menu_text, main_menu_text_rect),
                (Restart_button, restart_surface, restart_text_rect)]:
                
                if button_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, button_hover_color, button_rect)
                else:
                    pygame.draw.rect(self.screen, button_color, button_rect)

                self.screen.blit(button_text, button_text_rect)

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
    def check_collision(self, ball: Ball, pad: Pad, brick: Brick) -> tuple:

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
                self.countCollision[brickIndex] += 1  # Increment collision count

                # Check if the brick's hardness limit is reached
                if self.countCollision[brickIndex] >= collision[3]:
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
    
        if ball.y + ball.y_velocity > self.screen_height - ball.radius:
            Floor_collision = True
        if  Floor_collision:
            return (False,False,False,True)
        
        return (False,False,False,False) # No collision 


    #Level_up,Increase Speed and make bricks More harder
    def level_up(self):
        self.level += 1
        if self.level == 4:
            return
        self.speed += 3  # Increase pad speed
        self.ball.reset(self.Ball_X, self.Ball_Y)
        self.ball.increase_speed(2)  # Increase ball speed by 2 units
        self.pad.reset(self.screen_width, self.screen_height, self.Pad_Width, self.Pad_Height)
        self.bricks = Brick(self.level)
        self.countCollision= [0 for _ in range(0, (self.level + 2)*14)]
    
    # Game Loop
    def run(self):
        # Main game loop
        while not self.game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
            # Taking Input
            Key_press = pygame.key.get_pressed()
            if Key_press[pygame.K_SPACE]:
                self.game_start = True
            if Key_press[pygame.K_LEFT]and self.game_start:
                self.pad.move(-self.speed)
            elif Key_press[pygame.K_RIGHT]and self.game_start:
                self.pad.move(self.speed)
            # Move the ball
            if self.game_start:
                self.ball.move()
            #Check collision n Play Sound
            Collsion_Check = self.check_collision(self.ball, self.pad, self.bricks)
            if Collsion_Check[0]==1:
                self.Paddle_Hit.play()
            elif Collsion_Check[1]==1:
                self.Hit_Sound.play()
            elif Collsion_Check[2]==1:
                self.Break_Sound.play()
                self.score += 10
            elif Collsion_Check[3]==1:
                if self.lives>1:
                    self.Lost_life_sound.play()
                self.ball.reset(self.Ball_X,self.Ball_Y)
                self.pad.reset(self.screen_width,self.screen_height,self.Pad_Width,self.Pad_Height)
                self.lives-=1
                self.game_start=False

            #Check win
            if not self.bricks.brickCoordinates:
                self.level_up()    # We need better winning logic
                self.Win_sound.play()
                self.game_start=False
                return "level_complete"
            #Draw the Background
            self.screen.blit(self.Background, (0, 0))
            # Draw the ball
            self.ball.draw(self.screen)
            #Draw the pad
            self.pad.draw(self.screen)
            #Display Bricks
            self.bricks.displayBrick(self.screen)
            #Draw lives
            for i in range(self.lives):
                self.screen.blit(self.life_image, (self.life_x, self.life_y))
                self.life_x+=30
            self.life_x=10

            # Game_Over
            if self.lives<1:
                self.game_over=True
                self.Game_OV_Sound.play()

                if self.display_game_over(self.Game_OV_BG): # Returns true for game restart
                    self.game_over=False
                    self.game_start=False
                    return "restart"
                elif not self.main_menu():
                    return 'exit'
                else:
                    return 'restart'
                    
            self.clock.tick(60)
            # Display Score at bottom right corner
            score_text = self.small_text.render(f"Score: {self.score}", True, (144, 238, 144)) # soft green
            score_rect = score_text.get_rect(center=(self.screen_width - 100, self.screen_height - 50))
            self.screen.blit(score_text, score_rect)
            # Update the display
            pygame.display.flip()
            

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def display_you_won(self):
        """Display 'You Won' image that covers the entire background."""
        # Resize the image to fit the screen dimensions
        you_won_image = pygame.image.load("Assets/you_won.jpg").convert()
        you_won_image = pygame.transform.smoothscale(you_won_image, (self.screen_width, self.screen_height))

        # Display the resized image
        self.screen.blit(you_won_image, (0, 0))

        if self.score > self.highscore:
            highscore_message = self.small_font.render("New Highscore!", True, (144, 238, 144)) 
            highscore_rect = highscore_message.get_rect(center=(self.screen_width // 2, 50))  # Centered with y-offset of 50px
            self.screen.blit(highscore_message, highscore_rect)
                         
        pygame.display.flip()
        
        # Wait for a while before closing or going to main menu
        pygame.time.wait(3000)  # Display the image for 3 seconds
        if self.main_menu():
            return "play_again"

        
