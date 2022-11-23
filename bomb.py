import pygame
from pygame.sprite import Sprite
import time

class Bomb(Sprite):
    """This class manages bombs dropped by jet"""
    # Pass in the Sprite class to use its features
    # So we have to use the super init in our init

    def __init__(self, jet_fighter_game):
        """Create a bomb at the jets current location"""
        super().__init__()
        self.settings = jet_fighter_game.settings
        self.screen = jet_fighter_game.screen

        self.image = pygame.image.load('images/bomb_images/better_bomb.bmp')
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.rect = self.image.get_rect()

        self.start_pos_x = jet_fighter_game.jet.rect.x
        self.start_pos_y = jet_fighter_game.jet.rect.y + (jet_fighter_game.jet.rect.height/2)
        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y

        # Change in these speeds is only visiually noticable initially -
        # LATER SET THESE SPEEDS TO JET SPEED
        self.bomb_vertical_speed = 1.0
        self.bomb_horizontal_speed = 1.5

        # Acceleration paramater controls y component change and controls visual appareance of 'speed' of bomb
        # Bomb will 'fall' faster for higher acceleration number
        self.acceleration = .008

        # As drag constant increases the distance bomb travels in x increases over time
        # This is inverse what you would expect from a drag constant
        self.drag = .04
        # Redefining self.rect input here using pygame.Rect so spritecollideany function will work
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def free_fall(self):
        """Update the self.rect.x and y to create free fall effect"""
        self.rect.x += self.bomb_horizontal_speed
        self.bomb_horizontal_speed += self.drag * self.bomb_vertical_speed
        self.rect.y += self.bomb_vertical_speed**2
        self.bomb_vertical_speed += self.acceleration * self.bomb_vertical_speed

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
    def _check_any_collisions(self):
        """All bomb collision checks"""
        self._check_ground_collision()

    def _check_ground_collision(self):
        """Insert Explosion image if bomb hits ground and delete bomb"""
        # Threw in arbitrary number at end of equation to try and account for tanks being offset on ground for 3d effect
        if self.rect.y + self.rect.height >= self.settings.screen_height - self.settings.ground_height + 20:
            # Once bomb hits the ground 'explode'
            self.image = pygame.image.load('images/bomb_images/better_explosion.bmp')
            self.image = pygame.transform.scale(self.image, (100, 100))

    def update(self):
        """Call to freefall"""
        self._check_any_collisions()
        self.free_fall()

    def draw_bomb(self):
        """Draw the bomb to the screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))