import pygame
import math

class Enemy_Jet:
    """Class to manage the enemy jet"""
    def __init__(self, jet_fighter_game):
        """Initialize the jet and set its starting position"""
        # Pass in the screen dimensions from jet fighter game
        self.screen = jet_fighter_game.screen
        self.settings = jet_fighter_game.settings

        # Use the get_rect() method so we can access the screen dimensions and use them later
        self.screen_rect = jet_fighter_game.screen.get_rect()

        # Load the jet's image
        self.image = pygame.image.load('images/jet_images/enemy_plane.bmp')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.image = pygame.transform.flip(self.image, True, False)
        pygame.Surface.set_colorkey(self.image, (255, 255, 255))
        # Get the Jet's Rect so we can access and work with its dimmensions later
        self.rect = self.image.get_rect()

        self.start_pos_x = jet_fighter_game.settings.screen_width
        self.start_pos_y = int(jet_fighter_game.settings.screen_height/3)
        self.x = self.start_pos_x
        self.y = self.start_pos_y

        self.x_speed = 1.5


    def flight(self, time, friendly_missiles):
        """Method that makes the jet fly from right to left in sine path"""
        theta = .03 * time
        # Y Value set by sine function
        self.y = int(self.start_pos_y + 190*(math.sin(theta + 80)))

        # If the enemy plane's back edge hits the edge of the screen reset it to the right side
        if self.x <= 0 - self.rect.width:
            self.x = self.start_pos_x
        else:
            self.x -= self.x_speed

        missile_jet_collision = pygame.sprite.spritecollide(self, friendly_missiles, True)
        if missile_jet_collision:
            self.x = self.start_pos_x

    def blitme(self):
        """This is what will allow the jet to be drawn to the screen when we call from jet fighter game"""
        self.screen.blit(self.image, (self.x, self.y))