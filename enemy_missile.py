import pygame
from pygame.sprite import Sprite

class Enemy_Missile(Sprite):
    """This class manages missiles shot by enemy jet"""
    # Pass in the Sprite Class to access its featuress

    def __init__(self, jet_fighter_game):
        """Create a missile at the enemy jets current location"""
        super().__init__()
        self.settings = jet_fighter_game.settings
        self.screen = jet_fighter_game.screen

        self.image = pygame.image.load('images/jet_images/missile_transparent.png')
        self.image = pygame.transform.scale(self.image, (50, 45))
        self.image = pygame.transform.rotate(self.image,90)
        pygame.Surface.set_colorkey(self.image, (255,255,255))
        self.rect = self.image.get_rect()

        self.start_pos_x = jet_fighter_game.enemy_jet.rect.x
        self.start_pos_y = jet_fighter_game.enemy_jet.rect.y
        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y

        # Speed at which the missile will move across the screen
        self.missile_speed = 4.0

        # Flag to determine if to continue moving the missile and to determine if to draw an explosion
        self.friendly_missile_collision = False
        # I need a counter to keep track of the duration of time the explosion is drawn to the screen
        # I have to set to 1 initially to get the effect I want
        # If the counter is initially 0 then 0 % any integer will == 0
        self.explosion_counter = 1

    def update(self, friendly_missiles):
        """Check for collisons and move the missiles if there are none"""
        self._check_collisions(friendly_missiles)
        self._move_missile()
    def _check_collisions(self, friendly_missiles):
        # Look for a collision between self and the friendly missiles group, if there is one delete the friendly missile
        # then change the friendly missile collision flag to true
        friendly_missile_collision = pygame.sprite.spritecollide(self, friendly_missiles, True)
        if friendly_missile_collision:
            self.friendly_missile_collision = True
        # Now that the flag is changed I can check if the explosion has been on the screen for long enough, if it has call self.kill()
        if self.friendly_missile_collision and self.explosion_counter % 15 == 0:
            # kill the bomb/ explosion
            self.kill()
            # Reset the counter back to one if we reached the target number
            self.explosion_counter = 1


    def _move_missile(self):
        """Missile flies across the screen right to left"""
        # If the missile moves out of the screen delete it
        if self.rect.x + self.rect.width <= 0:
            self.kill()
        # If the missile and friendly missile collided then change the missile image to an explosion and start to
        # increment the explosion counter
        if self.friendly_missile_collision:
            self._explode()
            self.explosion_counter += 1
            print(self.explosion_counter)

        else:
            # If the missile has not exploded then move it from right to left across the screen at our specified speed
            self.rect.x -= self.missile_speed
            # Allow the missile to speed up over time
            self.missile_speed += .005 * self.missile_speed
    def _explode(self):
        """Change the image of the missile to an explosion"""
        self.image = pygame.image.load('images/bomb_images/tank_or_missile_explosion.png')
        self.image = pygame.transform.scale(self.image, (50, 45))
        # Now set the missiles
        # self.rect.y = self.start_pos_y
    def draw_missile(self):
        """Draw missile to the screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))