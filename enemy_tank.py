import pygame
from pygame.sprite import Sprite

class Enemy_Tank(Sprite):
    """Overall class to manage enemy tank attributes and actions"""
    def __init__(self, jet_fighter_game):
        """Initialize enemy tank by passing in screen dimensions used in game"""
        super().__init__()
        self.screen = jet_fighter_game.screen
        self.screen_width = jet_fighter_game.settings.screen_width
        self.screen_height = jet_fighter_game.settings.screen_height
        self.screen_rect = jet_fighter_game.screen.get_rect()

        self.image = pygame.image.load('images/tank_images/American_sherman_attack_1.bmp').convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (70,70))
        # Still need to mirror tank so that its orriented the right direction

        self.rect = self.image.get_rect()
        # Start position is the length of the tank past the screen width so the tank passes fully into view
        self.start_pos_x = self.screen_width - self.rect.width
        # Start position for the y of the tank is the ground - an arbitrary number that makes the tank sit offset "in"
        # the ground for a better 3D effect
        self.start_pos_y = self.screen_height - jet_fighter_game.ground.rect.height - 15
        # Start the tank's x position at the start position
        self.rect.x = self.start_pos_x

    def update(self, tank_speed):
        """Move Tanks"""
        self.move_tank(tank_speed)

    def move_tank(self, tank_speed):
        """Function to move tank"""
        # Only move the tank if the
        self.rect.x -= tank_speed
        self.rect.y = self.start_pos_y
        # Creating this Rect attribute so collision will run
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def draw_tank(self):
        """Function to draw tank to screen"""
        self.screen.blit(self.image, self.rect)