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
        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y

        self.x_speed = 1.5


    def flight(self, time, friendly_missiles):
        """Method that makes the jet fly from right to left in sine path"""
        # scale theta by a small decimal to give the effect of infinitesimally hitting every theta value on the sign curve
        #   so that the flight path appears continuous
        theta = .03 * time

        # Y Value set by sine function
        self.rect.y = int(self.start_pos_y + 190*(math.sin(theta + 80)))

        # If the enemy plane's back edge hits the edge of the screen reset it to the right side
        if self.rect.x <= 0 - self.rect.width:
            self.reset_jet()
        else:
            self.rect.x -= self.x_speed

        # Check if the friendly missiles have collided with the enemy, if so restart enemy plane at edge of screen
        missile_jet_collision = pygame.sprite.spritecollide(self, friendly_missiles, True)
        if missile_jet_collision:
            self.reset_jet()

        # speed up the speed of the enemy jet over time until it reaches a max speed that makes the game reasonably difficult
        #   we evaluate the time from our main game loop counter thats passed into this method
        if (time % 500) == 0:
            # Max speed out at 2.5
            if self.x_speed >= 4.0:
                self.x_speed = 4.0
            else:
                self.x_speed += 0.25



    def reset_jet(self):
        """When the leftmost of the jet hits the leftmost side of the screen reset the jet to the right side"""
        # Making this a method so that I can call it from within the main game
        self.rect.x = self.start_pos_x
        # Reset to the start height as well
        self.rect.y = self.start_pos_y
    def blitme(self):
        """This is what will allow the jet to be drawn to the screen when we call from jet fighter game"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
