import pygame
class Pad:
    def __init__(self, img, width, height, padWidth, padHeight):
        self.x = (width - padWidth) // 2
        self.y = height - padHeight - 50
        self.width = width
        self.padWidth = padWidth
        self.padHeight = padHeight
        
        # Load and scale the pad image
        self.image = pygame.transform.scale(pygame.image.load(img), (padWidth, padHeight))
        
        # Create a mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dx):
        self.x += dx
        # Keep the pad within the screen bounds
        if self.x < 5:
            self.x = 5
        elif self.x+5 >self.width-self.padWidth:
            self.x = self.width - self.padWidth - 5

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))