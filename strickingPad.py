import pygame
class Pad:
    def __init__(self,width,height,padWidth,padHeight,color):
        self.x = (width - padWidth) // 2
        self.y = height - padHeight - 15
        self.width = width
        self.padWidth = padWidth
        self.padHeight = padHeight
        self.color = color

    def move(self, dx):
        self.x += dx
        # Keep the pad with in the screen
        if self.x < 5:
            self.x = 5
        elif self.x + 5 > self.width - self.padWidth:
            self.x = self.width - self.padWidth - 5

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.padWidth, self.padHeight))