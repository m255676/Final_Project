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

        self.image = pygame.image.load('images/jet_images/enemy_missile.png')
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.image = pygame.transform.rotate(self.image,90)
        pygame.Surface.set_colorkey(self.image, (255,255,255))
        self.rect = self.image.get_rect()

        self.start_pos_x = jet_fighter_game.enemy_jet.rect.x
        self.start_pos_y = jet_fighter_game.enemy_jet.rect.y
        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y

        self.missile_speed = 4.0

    def _move_missile(self):
        """Missile flies across the screen right to left"""
        self.rect.x -= self.missile_speed
        self.missile_speed += .005 * self.missile_speed

    def update(self):
        """Call missile move"""
        self._move_missile()

    def draw_missile(self):
        """Draw missile to the screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))