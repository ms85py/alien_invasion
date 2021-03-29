
import pygame.font


class Button:

    def __init__(self, ai_game, msg):
        """initializing button attribs"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # button size and properties
        self.width, self.height = 200, 75
        self.button_color = (128, 128, 128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('arial', 50)

        # creating rect of button and centering it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # setting button text once
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        """turning a msg into a rendered img, centering txt on button"""
        self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center


    def draw_button(self):
        """drawing empty button and adding text to it"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)
