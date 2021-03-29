
import pygame

from pygame.sprite import Sprite


class Ship(Sprite):
    """class to manage the player ship"""
    # second arg is an instance of the alien invasion game
    def __init__(self, ai_game):
        """initialize ship and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # loading the ship bmp and setting its rectangle
        self.image = pygame.image.load('images/ship2.png')
        self.rect = self.image.get_rect()

        # placing new ship in the middle of the bottoms screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 25

        # saving a value for the ships mid-point
        self.x = float(self.rect.x)

        # movement flags
        self.moving_right = False
        self.moving_left = False


    def center_ship(self):
        """centers players ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 25
        self.x = float(self.rect.x)


    def update(self):
        """updating ships pos based on movement flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # actualizing the rect-obj to self.x
        self.rect.x = self.x


    def blitme(self):
        """drawing the ship at its current location"""
        self.screen.blit(self.image, self.rect)
