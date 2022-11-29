import sys
import pygame
from jet import Jet
from settings import Settings
from ground import Ground
from enemy_tank import Enemy_Tank
from bomb import Bomb
from enemy_jet import Enemy_Jet
from enemy_missile import Enemy_Missile
from friendly_missile import Friendly_Missile
from button import PlayButton
from button import PauseButton
import time
import math

class JetFighterGame:
    """Overall Class to manage game assests and behaviors"""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Jet Fighter Game")
        self.back_ground = pygame.image.load('images/blue_sky_background.bmp')
        self.back_ground = pygame.transform.scale(self.back_ground, (self.settings.screen_width, self.settings.screen_height))

        self.loop_speed = 80
        self.counter = 0

        self.jet = Jet(self)
        self.enemy_jet = Enemy_Jet(self)
        self.ground = Ground(self)

        self.bombs = pygame.sprite.Group()
        self.enemy_tanks = pygame.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()
        self.friendly_missiles = pygame.sprite.Group()

        self.game_active = False
        self.game_paused = False

        self.play_button = PlayButton(self, "Single Player")
        self.pause_button = PauseButton(self, "!!")

    def run_game(self):
        """This is the main loop for the game"""
        # Need to make an instance of the first tank to run before the counter starts making new tanks
        first_tank = Enemy_Tank(self)
        self.enemy_tanks.add(first_tank)

        # Run while the game is not running
        # Still need to be able to check for events
        # Still need to draw the start game features: Single/ Multiplayer, Credits
        while not self.game_active:
            # Check for any key events
            self._check_events()
            self._update_screen()

        # Run the game if the game has been set to active, when the play button has been clicked
        while self.game_active:
            # Run the game while the game is not paused
            if not self.game_paused:
                self._check_events()
                self.enemy_jet.flight(self.counter, self.friendly_missiles)
                # This will move the tanks
                self.enemy_tanks.update()
                # This will update the bombs in our sprite group
                self.bombs.update()
                # Check Ground Collisions
                self._check_ground_collision()
                # Track Time using a counter
                self.counter += 1
                if (self.counter % 300 == 0):
                # After certain time make tanks
                    self._make_new_tanks()
                if (self.counter % 175 == 0):
                # After certain time make enemy jet shoot missiles
                    self._shoot_enemy_missile()
                # update the missiles so they travel across the screen.
                self.enemy_missiles.update()
                self.friendly_missiles.update()
                # This will call the jet movement function
                self.jet.move_jet(self.enemy_missiles, self.friendly_missiles, self.bombs, self.enemy_tanks)


                # Control FPS
                self.clock.tick(self.loop_speed)
                # Update Screen
                self._update_screen()

            # If the game is just continue to draw everything at its last position
            # and continue to look for events in order to exit or unpause the game
            elif self.game_paused:
                self._check_events()
                self._update_screen()


    def _check_events(self):
        """This method responds to key events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for mouse button down event and log the position of it
                #       so that we can check for the button being 'clicked' in our check play button function
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_pause_button(mouse_pos)

    def _check_keydown_events(self, event):
        """This method responds to keypresses"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_UP:
            self.jet.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.jet.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._drop_bomb()
        elif event.key == pygame.K_RIGHT:
            self.jet.speeding_up = True
        elif event.key == pygame.K_LEFT:
            self._shoot_friendly_missile()

    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player clicks Play"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # Only start the game if the game is not running and the button is clicked
        # These conditions mean that the game won't restart if the button area is accidentally clicked in game
        if play_button_clicked and not self.game_active:
            self.game_active = True

    def _check_pause_button(self, mouse_pos):
        """ Pause the game if the game is not already paused"""
        pause_button_clicked = self.pause_button.rect.collidepoint(mouse_pos)
        if pause_button_clicked and not self.game_paused:
            self.game_active = True
            self.game_paused = True
        # If the pause button is clicked while the game is already paused then unpause the game
        elif pause_button_clicked and self.game_paused:
            self.game_paused = False

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.jet.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.jet.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.jet.speeding_up = False

    def _make_new_tanks(self):
        """After counter hits target number/ after desired elapsed time, make a new tank"""
        new_enemy_tank = Enemy_Tank(self)
        self.enemy_tanks.add(new_enemy_tank)
    def _shoot_enemy_missile(self):
        """"After counter hits target number/ after desired elapsed time, make a new missile"""
        new_enemy_missile = Enemy_Missile(self)
        self.enemy_missiles.add(new_enemy_missile)
    def _shoot_friendly_missile(self):
        """On key event make a missile instance and add to group to be updated in game loop"""
        new_friendly_missile = Friendly_Missile(self)
        self.friendly_missiles.add(new_friendly_missile)

    def _drop_bomb(self):
        """Create a new bomb and add it to the Sprite group"""
        new_bomb = Bomb(self)
        self.bombs.add(new_bomb)

    def _check_ground_collision(self):
        """Check if the bomb's ground collision flag is true and delete bomb if it is"""
        for bomb in self.bombs.sprites():
            if bomb.ground_collision:
                bomb.kill()

    def _update_screen(self):
        """This method updates the screen"""
        self.screen.blit(self.back_ground, (0,0))
        self.ground.blitme()
        self.jet.blitme()
        self.enemy_jet.blitme()
        for enemy_missile in self.enemy_missiles.sprites():
            enemy_missile.draw_missile()

        for friendly_missile in self.friendly_missiles.sprites():
            friendly_missile.draw_missile()

        for enemey_tank in self.enemy_tanks.sprites():
            enemey_tank.draw_tank()

        for bomb in self.bombs.sprites():
            bomb.draw_bomb()

        # Draw a red backdrop if the game has not started yet
        if not self.game_active:
            self.screen.fill((0, 0, 0))

        # Draw the play button if the game is not active
        if not self.game_active:
            self.play_button.draw_button()

        # Draw the pause button
        self.pause_button.draw_button()

        # Makes the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    play_game = JetFighterGame()
    play_game.run_game()
