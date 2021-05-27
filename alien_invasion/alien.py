import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ A single alien"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load alien image and set position
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # set the position to top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # save horizontal position
        self.x = float(self.rect.x)
    
    def update(self):
        """ make aliens move to the right"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """if aliens touch the edge of the screen return True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
