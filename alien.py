
import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """a class to represent a single alien of a fleet"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # loading UFO and sets its rect
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()

        # placing each new UFO at top left with spacing of 1x UFO
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # saving exact pos of UFO, we only need x because we'll only care about the horizontal movement
        self.x = float(self.rect.x)


    def check_edges(self):
        """returns True is alien hits the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """moving the alien to the right or left side"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

