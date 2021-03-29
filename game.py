
import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """class to manage game assets and behavior"""
    def __init__(self):
        # pygame instance
        pygame.init()

        # settings instance
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("alien invasion thingy")

        # instance to save stats and show it on the screen
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # ship instance + bullet group
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # alien group
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # creates the 'play' button
        self.play_button = Button(self, "PLAY")



    def run_game(self):
        """main loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _check_events(self):
        """checks and responds to keyboard/mouse input"""
        for event in pygame.event.get():
            # quit stuff
            if event.type == pygame.QUIT:
                sys.exit()
            # mouse click for 'PLAY' button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            # checks for key down/up events and sends it to appropriate method
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """catches key down event and sets movement flags"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()


    def _check_keyup_events(self, event):
        """catches key up event and sets movement flags"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _check_play_button(self, mouse_pos):
        """start a new game when clicking play"""
        # checking if button is clicked while there's no game active
        # else the button would be clickable even after turning invisible
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # resets games speed
            self.settings.initialize_dynamic_settings()

            # reset stats / level / ships and changing game state
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # getting rid of alien ships and bullets
            self.aliens.empty()
            self.bullets.empty()

            # creating new fleet and centering players ship
            self._create_fleet()
            self.ship.center_ship()

            # making mouse pointer invisible
            pygame.mouse.set_visible(False)


    def _fire_bullet(self):
        """creating and adding bullet to bullet group"""
        if len(self.bullets) < self.settings.bullets_max:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """updates pos of bullets and removes old ones"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()


    def _check_bullet_alien_collision(self):
        """responds to bullet-alien collisions"""
        # checks if a bullet hits an alien
        # if it did, the bullet + alien will be removed
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # adds points to score on collision
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            # high score renewal if score > high score
            self.sb.check_high_score()

        # removes bullets and creates new fleet - also
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            # if alien fleet is ...exterminated, increase speed
            self.settings.increase_speed()

            # increases level by 1
            self.stats.level += 1
            self.sb.prep_level()


    def _create_alien(self, alien_number, row_number):
        """creating an alien an placing it into the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien = Alien(self)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _create_fleet(self):
        """creates a fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # leaving a width of an UFO as space on left/right side of screen
        available_space_x = self.settings.screen_width - (2 * alien_width)

        # calculating the spacing between UFOs
        number_aliens_x = available_space_x // (2 * alien_width)

        # calculating the vertical space by taking screen height and subtracting
        # UFO row height from top + our own ships height from bottom
        # then further subtract 2x UFO height
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (2 * alien_height) - ship_height

        # we also want some space under the last row of aliens
        # so to calculate the number of rows we divide the screen space left by 2 * UFO height
        number_rows = available_space_y // (2 * alien_height)

        # creating a fleet of UFOs
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _update_aliens(self):
        """checks if fleet is at an edge, then updates pos"""
        self._check_fleet_edges()
        self.aliens.update()

        # checking for collisions between aliens and player ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # checks if aliens hit the bottom of the screen
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        """checks if alien fleet hit an edge and acts accordingly"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """drops entire fleet and changes its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        """responds to ship being hit by aliens"""
        # takes one life away if there's lives left
        # also removes that life from the scoreboard
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # removes alien fleet + leftover bullets
            self.aliens.empty()
            self.bullets.empty()

            # creates a new fleet and centers players ship
            self._create_fleet()
            self.ship.center_ship()

            # stops game for a short while
            sleep(1.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """...weird name, I know
        but it simply checks if any alien ship has reached the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _update_screen(self):
        """draws screen on each iteration of the main loop"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # ignore unresolved reference below, we're using the method from Bullets, not Sprite. Pycharm...sigh.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # drawing the aliens
        self.aliens.draw(self.screen)

        # drawing information about the score
        self.sb.show_score()

        # draws play-button on inactive game state
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


# creating instance and starting the game if file is run
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
