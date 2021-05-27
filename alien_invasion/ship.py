import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # align ship to the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # save ship position as float number
        self.x = float(self.rect.x)

        # move ship
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #update ship's rect
        self.rect.x = self.x

    def center_ship(self):
        """ put ship to the center bottom of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)