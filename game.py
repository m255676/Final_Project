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

        self.loop_speed = 100

        # Create an instance of the jet class and pass in self
        #   so attributes can be passed into the class to be used by it
        self.jet = Jet(self)
        self.ground = Ground(self)
        self.enemy_tank = Enemy_Tank(self)
        self.bomb = Bomb(self)

    def run_game(self):
        """This is the main loop for the game"""
        while True:
            self._check_events()
            # This will call the jet movement function
            self.jet.move_jet()
            self.enemy_tank.move_tank()
            self.bomb.free_fall()
            self._update_screen()

            self.clock.tick(self.loop_speed)

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
        elif event.key == pygame.K_1:
            self.jet.moving_up = True
        elif event.key == pygame.K_0:
            self.jet.moving_down = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_1:
            self.jet.moving_up = False
        elif event.key == pygame.K_0:
            self.jet.moving_down = False

    def _update_screen(self):
        """This method updates the screen"""
        screen_color = (158, 207, 230) #Later move to settings
        self.screen.fill(screen_color)
        self.ground.draw_ground()
        self.jet.blitme()
        self.enemy_tank.draw_tank()
        self.bomb.draw_bomb()
        # Makes the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    play_game = JetFighterGame()
    play_game.run_game()
