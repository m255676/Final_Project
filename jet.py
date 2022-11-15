import pygame
from pygame.sprite import Sprite

class Jet:
    """Class to manage Jet gameplay"""
    def __init__(self, jet_fighter_game):
        """Initialize the jet and set its starting position"""
        # Pass in the screen dimensions from jet fighter game
        self.screen = jet_fighter_game.screen
        self.settings = jet_fighter_game.settings

        # Use the get_rect() method so we can access the screen dimensions and use them later
        self.screen_rect = jet_fighter_game.screen.get_rect()

        # Load the jet's image
        self.image = pygame.image.load('images/jet_images/AEG_CIV_attack_1.bmp')
        self.image = pygame.transform.scale(self.image, (80,80))
        # Get the Jet's Rect so we can access and work with its dimmensions later
        self.rect = self.image.get_rect()

        # Store a decimal value for the jet's horizontal position
        self.x = float(self.rect.x)
        # Store a decimal value for the jet's vertical position
        self.y = float(self.rect.y)

        # Flags that will be changed in keydown/ups in order to have continous movement for duration of keydown
        self.moving_up = False
        self.moving_down = False

    def fly_right(self):
        """Method that will move the jet rightward on the screen"""
        jet_speed = 1.0
        # Check if the jet is at the right edge, if it is reset to the left side before flying right
        if self.rect.x > self.settings.screen_width:
            self._reset_jet()
        else:
            self.rect.x += jet_speed
            self.increase_altitude()
            self.decrease_altitude()

    def increase_altitude(self):
        """This will increase the altitude of the jet"""
        # Only increase altitude when not at top of screen
        jet_speed = 10.0
        if self.rect.y > 0 and self.moving_up:
            self.rect.y -= jet_speed

    def decrease_altitude(self):
        """This will decrease the altitude of the jet"""
        # Only decrease if not below bottom third of screen
        jet_speed = 10.0
        if self.rect.y < self.settings.screen_height * 2/3 and self.moving_down:
            self.rect.y += jet_speed

    def _reset_jet(self):
        """Method to return the jet to the left of the screen"""
        self.rect.x = self.rect.height

    def blitme(self):
        """This is what will allow the jet to be drawn to the screen when we call from jet fighter game"""
        self.screen.blit(self.image, self.rect)