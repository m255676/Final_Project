import pygame
import math
from explosion import Explosion

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

        # I always want to start the enemy jet at its width away from the edge of the scree so it flies into view
        # and I want the y position to always be 1/3 of the way down the screen
        self.start_pos_x = jet_fighter_game.settings.screen_width + self.rect.width
        self.start_pos_y = int(jet_fighter_game.settings.screen_height/3)
        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y

        # This speed will determine how fast the jet moves in the x direction/ how fast it moves through its sine path
        self.x_speed = 1.5
        self.new_explosion = Explosion(self)
        self.new_explosions_group = pygame.sprite.Group()

    def flight(self, time, friendly_missiles):
        """Method that makes the jet fly from right to left in sine path"""
        # scale theta by a small decimal to give the effect of infinitesimally hitting every theta value on the sign
        # curve so that the flight path appears continuous
        theta = .03 * time

        # Y Value set by sine function
        self.rect.y = int(self.start_pos_y + 190*(math.sin(theta + 80)))

        # If the enemy plane's back edge hits the edge of the screen reset it to the right side
        if self.rect.x <= 0 - self.rect.width:
            self.reset_jet()
        else:
            # Otherwise while the plane is on the screen continue to move it
            self.rect.x -= self.x_speed

        # Check if the friendly missiles have collided with the enemy, if so restart enemy plane at edge of screen
        missile_jet_collision = pygame.sprite.spritecollide(self, friendly_missiles, True)
        if missile_jet_collision:
            # Make an explosion where the jet was hit
            new_explosion = Explosion(self)
            self.new_explosions_group.add(new_explosion)
            self.reset_jet()

        # Call the new_explosions lifespan function and draw it to the screen until it dies
        self.new_explosions_group.draw(self.screen)
        self.new_explosions_group.update()

        # speed up the speed of the enemy jet over time until it reaches a max speed that makes the game reasonably
        # difficult
        # we evaluate the time from our main game loop counter which is passed into this method
        if (time % 300) == 0:
            # Max speed out at 2.5
            if self.x_speed >= 4.0:
                self.x_speed = 4.0
            else:
                self.x_speed += 0.50



    def reset_jet(self):
        """When the leftmost of the jet hits the leftmost side of the screen reset the jet to the right side"""
        # Making this a method so that I can call it from within the main game
        self.rect.x = self.start_pos_x
        # Reset to the start height as well
        self.rect.y = self.start_pos_y
    def blitme(self):
        """This is what will allow the jet to be drawn to the screen when we call from jet fighter game"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
