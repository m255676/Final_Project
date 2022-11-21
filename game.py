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

        # Create an instance of the jet class and pass in self
        #   so attributes can be passed into the class to be used by it
        self.jet = Jet(self)
        self.ground = Ground(self)

        #self.enemy_tank = Enemy_Tank(self)

        self.bombs = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()

    def run_game(self):
        """This is the main loop for the game"""

        while True:
            self._check_events()
            # This will call the jet movement function
            self.jet.move_jet()
            # Moves first tank
            #self.enemy_tank.move_tank()
            # Makes a new tank after a certain time
            #self._make_new_tanks()
            # Move every tank in our sprite group
            #self.tanks.update()
            # Move every bomb in our sprite group
            self.bombs.update()

            self._update_screen()
            # Control FPS
            self.clock.tick(self.loop_speed)
            # Track Time using a counter
            self.counter += 1

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
        if (self.counter % 10000 == 0):
            new_tank = Enemy_Tank(self)
            self.tanks.add(new_tank)
            self.counter = 0
    def _drop_bomb(self):
        """Create a new bomb and add it to the Sprite group"""
        new_bomb = Bomb(self)
        self.bombs.add(new_bomb)

    def _update_screen(self):
        """This method updates the screen"""
        #screen_color = (158, 207, 230) #Later move to settings
        self.screen.blit(self.back_ground, (0,0))
        self.ground.draw_ground()
        self.jet.blitme()
        #self.enemy_tank.draw_tank()
        #for tank in self.tanks.sprites():
            #tank.draw_tank()
        for bomb in self.bombs.sprites():
            bomb.draw_bomb()
        # Makes the most recently drawn screen visible
        pygame.display.flip()









if __name__ == '__main__':
    # Make a game instance and run the game
    play_game = JetFighterGame()
    play_game.run_game()
