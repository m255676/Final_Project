import pygame

class Enemy_Tank():
    """Overall class to manage enemy tank attributes and actions"""

    def __init__(self, jet_fighter_game):
        """Initialize enemy tank by passing in screen dimensions used in game"""
        self.screen = jet_fighter_game.screen
        self.screen_width = jet_fighter_game.settings.screen_width
        self.screen_height = jet_fighter_game.settings.screen_height
        self.screen_rect = jet_fighter_game.screen.get_rect()

        self.image = pygame.image.load('images/tank_images/sample_tank.bmp')
        self.image = pygame.transform.scale(self.image, (60,40))
        # Still need to mirror tank so that its orriented the right direction

        self.rect = self.image.get_rect()

        self.start_pos_x = self.screen_width - self.rect.width
        self.start_pos_y = self.screen_height - jet_fighter_game.ground.rect_height - self.rect.height

        self.rect.x = self.start_pos_x

    def move_tank(self):
        """Function to move tank"""
        self.rect.x -= 1.0

    def draw_tank(self):
        """Function to draw tank to screen"""
        self.screen.blit(self.image, (self.rect.x, self.start_pos_y))