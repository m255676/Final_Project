import pygame
from pygame.sprite import Sprite

class Bomb(Sprite):
    """This class manages bombs dropped by jet"""
    # Pass in the Sprite class to use its features
    # So we have to use the super init in our init

    def __init__(self, jet_fighter_game):
        """Create a bomb at the jets current location"""
        super().__init__()
        self.settings = jet_fighter_game.settings
        self.screen = jet_fighter_game.screen

        self.image = pygame.image.load('images/bomb_images/Bomb_1.bmp')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        self.start_pos_x = jet_fighter_game.jet.rect.x
        self.start_pos_y = jet_fighter_game.jet.rect.y

        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y
        self.bomb_vertical_speed = 2.0

        # Use this elapsed time number for trig calculations
        self.loop_speed = jet_fighter_game.loop_speed
        self.t_old = pygame.time.get_ticks()
        self.GRAVITY = 2.0

    def free_fall(self):
        """Update the self.rect.x and y to create free fall effect"""
        bomb_horizontal_speed = 1.0
        #calc_x = (self.start_pos_x + bomb_horizontal_speed * (self.t))
        #calc_y = (self.start_pos_y + (0.5 * self.GRAVITY * self.t**2))
        self.t = self.t_old - pygame.time.get_ticks()/1000
        self.rect.x = self.t
        self.rect.y = self.t ** 2
        print(self.rect.x)
        #print(self.rect.y)
    def draw_bomb(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))