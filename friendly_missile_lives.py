import pygame
from pygame.sprite import Sprite

class FriendlyMissileLives(Sprite):
    """Overall class to manage the pictures of the friendly missiles that show num missiles available"""
    def __init__(self, jet_fighter_game):
        """Initialize each missile by passing in screen dimensions used in game"""
        super().__init__()
        self.screen = jet_fighter_game.screen
        self.screen_rect = jet_fighter_game.screen.get_rect()

        # Set the image of our sprite to the image we use for the jet
        self.image = pygame.image.load('images/jet_images/missile_transparent.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 55))

        # Establish our rectangle attributes from the image rectangele
        self.rect = self.image.get_rect()


    def draw_life(self):
        """Function to missile life to screen"""
        self.screen.blit(self.image, self.rect)