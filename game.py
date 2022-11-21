import sys
import pygame
from jet import Jet
from settings import Settings
from ground import Ground
from enemy_tank import Enemy_Tank
from bomb import Bomb
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

        self.loop_speed = 100
        self.counter = 0

        self.jet = Jet(self)
        self.ground = Ground(self)
        self.bombs = pygame.sprite.Group()
        self.enemy_tanks = pygame.sprite.Group()

    def run_game(self):
        """This is the main loop for the game"""
        # Need to make an instance of the first tank to run before the counter starts making new tanks
        first_tank = Enemy_Tank(self)
        self.enemy_tanks.add(first_tank)
        while True:
            # Check for any key events
            self._check_events()
            # This will call the jet movement function
            self.jet.move_jet()
            # This will update the bombs in our sprite group
            self.bombs.update()
            # This will move the tanks
            self.enemy_tanks.update()
            # Track Time using a counter
            self.counter += 1
            if (self.counter % 500 == 0):
                self._make_new_tanks()
            # Control FPS
            self.clock.tick(self.loop_speed)

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

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.jet.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.jet.moving_down = False

    def _make_new_tanks(self):
        """After counter hits target number/ after desired elapsed time, make a new tank"""
        new_enemy_tank = Enemy_Tank(self)
        self.enemy_tanks.add(new_enemy_tank)
        self.counter = 0

    def _drop_bomb(self):
        """Create a new bomb and add it to the Sprite group"""
        new_bomb = Bomb(self)
        self.bombs.add(new_bomb)

    def _update_screen(self):
        """This method updates the screen"""
        self.screen.blit(self.back_ground, (0,0))
        self.ground.draw_ground()
        self.jet.blitme()
        for enemey_tank in self.enemy_tanks.sprites():
            enemey_tank.draw_tank()
        for bomb in self.bombs.sprites():
            bomb.draw_bomb()
        # Makes the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    play_game = JetFighterGame()
    play_game.run_game()
