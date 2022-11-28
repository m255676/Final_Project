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

    def run_game(self):
        """This is the main loop for the game"""
        # Need to make an instance of the first tank to run before the counter starts making new tanks
        first_tank = Enemy_Tank(self)
        self.enemy_tanks.add(first_tank)
        while True:
            # Check for any key events
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
        elif event.key == pygame.K_RIGHT:
            self.jet.speeding_up = True
        elif event.key == pygame.K_LEFT:
            self._shoot_friendly_missile()

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
        # Makes the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    play_game = JetFighterGame()
    play_game.run_game()
