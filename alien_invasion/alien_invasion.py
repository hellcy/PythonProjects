import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:

    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()

        # Full Screen
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # create play button, to display it on the screen
        # need to call draw_button method when screen updates
        self.play_button = Button(self, "Play")

        pygame.display.set_caption('Alien Invasion')

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._check_play_button(enter_or_space=True)
            self._fire_bullet() 
        elif event.key == pygame.K_RETURN:
            self._check_play_button(enter_or_space=True)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos=(0, 0), enter_or_space=False):
        """ start the game when user click the button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) or enter_or_space
        if  button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True

            # clear bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

    def _update_bullets(self):
        self.bullets.update()

        # delete bullet outside of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check if bullets hit aliens, remove bullets and aliens from the group
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        # update score when there is a collision
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        # if no aliens (all have been killed), clear the bullets and create new fleet
        if not self.aliens:
            # delete all current bullets and create another fleet
            self.bullets.empty()
            self._create_fleet()

            # increase game difficulty
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """ check if any alien is at the edge of the screen and update position"""
        self._check_fleet_edges()
        self.aliens.update()

        # check if aliens hit the ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # check if aliens have reached the bottom
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """check if any aliens touch the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """move down the entire fleet and change the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # render the new screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.scoreboard.show_score()

        # display the Play button when game is not active
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """create a new bullet, add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        # create the first alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # caluclate number of aliens for each row
        available_space_x = self.settings.screen_width -  (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # calculate number of rows
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create a row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """ create a alien in the current row"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _ship_hit(self):
        """ response when ship was hit by alien"""
        if self.stats.ships_left > 0:  
            # decrement ship
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # clear aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet and ship
            self._create_fleet()
            self.ship.center_ship()

            # pause the game for a while
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """ check if any aliens have reached the bottom of screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()