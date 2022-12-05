import random

import pygame
import math
from explosion import Explosion
from random import randint
class PowerUp:
    """Class to manage the enemy jet"""
    def __init__(self, jet_fighter_game, height):
        """Initialize the jet and set its starting position"""
        # Pass in the screen dimensions from jet fighter game
        self.screen = jet_fighter_game.screen
        self.settings = jet_fighter_game.settings

        # Use the get_rect() method so we can access the screen dimensions and use them later
        self.screen_rect = jet_fighter_game.screen.get_rect()

        # Load the jet's image
        self.image = pygame.image.load('images/bomb_images/power_up.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        # Get the Jet's Rect so we can access and work with its dimmensions later
        self.rect = self.image.get_rect()

        # I always want to start the enemy jet at its width away from the edge of the scree so it flies into view
        # and I want the y position to always be the random input
        # I also offset an additional 20 so that the sine curve will never be in sequence with the enemy jet
        self.start_pos_x = jet_fighter_game.settings.screen_width + self.rect.width + 20
        self.start_pos_y = height
        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y

        # This speed will determine how fast the jet moves in the x direction/ how fast it moves through its cos path
        self.x_speed = 2.0

        # Initialize an instance of the explosion and make an empty explosions group
        self.new_explosion = Explosion(self)
        self.new_explosions_group = pygame.sprite.Group()

    def flight(self, time, friendly_missiles):
        """Method that makes the jet fly from right to left in sine path"""
        # scale theta by a small decimal to give the effect of infinitesimally hitting every theta value on the sign
        # curve so that the flight path appears continuous
        theta = .03 * time

        # Y Value set by sine function
        self.rect.y = int(self.start_pos_y + 150*(math.sin(theta + 200)))

        self.rect.x -= self.x_speed

        # Check if the friendly missiles have collided with the enemy, if so restart enemy plane at edge of screen
        missile_power_up_collision = pygame.sprite.spritecollide(self, friendly_missiles, True)
        if missile_power_up_collision:
            # Make an explosion where the jet was hit
            new_explosion = Explosion(self)
            self.new_explosions_group.add(new_explosion)
            self.take_out_of_view()
            # Increase the lives left by one when the power up is hit and lives left is less than three
            if self.settings.lives_left < 3:
                self.settings.lives_left += 1

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
    def reset_power_up(self):
        """Function that will bring the power up back into view at a randomized height that"""
        self.rect.y = random.randint(100, self.settings.screen_height - 100)
        self.rect.x = self.start_pos_x
    def take_out_of_view(self):
        """Since I can't delete the power up I'll just move it out of view until I need to reset it again"""
        self.rect.x = -100
    def blitme(self):
        """This is what will allow the jet to be drawn to the screen when we call from jet fighter game"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
