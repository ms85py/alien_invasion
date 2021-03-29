
import pygame

# importing Sprite to use as parent for the bullet class
from pygame.sprite import Sprite


class Bullet(Sprite):
    """manages bullets fired from the ship"""
    def __init__(self, ai_game):
        # super init to inherit from Sprite
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # creates a bullet at (0, 0) and then move it to the right position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # saving bullet pos
        self.y = float(self.rect.y)


    def update(self):
        """moving bullet"""
        # updates the bullet pos
        self.y -= self.settings.bullet_speed
        # updates the rect pos
        self.rect.y = self.y


    def draw_bullet(self):
        """drawing the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

