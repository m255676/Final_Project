import pygame
from pygame.sprite import Sprite

class BombLives(Sprite):
    """Overall class to manage the pictures of the bombs that show num bombs available"""
    def __init__(self, jet_fighter_game):
        """Initialize each bomb by passing in screen dimensions used in game"""
        super().__init__()
        self.screen = jet_fighter_game.screen
        self.screen_rect = jet_fighter_game.screen.get_rect()

        # Set the image of our sprite to the image we use for the jet
        self.image = pygame.image.load('images/bomb_images/bomb.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Establish our rectangle attributes from the image rectangele
        self.rect = self.image.get_rect()


    def draw_life(self):
        """Function to draw tank to screen"""
        self.screen.blit(self.image, self.rect)