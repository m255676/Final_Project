import pygame
from pygame.sprite import Sprite
from time import sleep
class Bomb(Sprite):
    """This class manages bombs dropped by jet"""
    # Pass in the Sprite class to use its features
    # So we have to use the super init in our init

    def __init__(self, jet_fighter_game):
        """Create a bomb at the jets current location"""
        super().__init__()
        self.settings = jet_fighter_game.settings
        self.screen = jet_fighter_game.screen

        self.image = pygame.image.load('images/bomb_images/bomb.png')
        pygame.Surface.set_colorkey(self.image, (255, 255, 255))
        pygame.Surface.set_colorkey(self.image, (238, 238, 238))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        # Need to know the ground with so I can set the explosions at the same y pos that the tanks are placed at
        # and the tanks are placed relative to the ground height
        self.ground_height = jet_fighter_game.settings.ground_height
        self.start_pos_x = jet_fighter_game.jet.rect.x
        self.start_pos_y = jet_fighter_game.jet.rect.y + (jet_fighter_game.jet.rect.height/2)
        self.rect.x = self.start_pos_x
        self.rect.y = self.start_pos_y

        # Change in these speeds is only visiually noticable initially -
        # LATER SET THESE SPEEDS TO JET SPEED
        self.bomb_vertical_speed = 2.25
        self.bomb_horizontal_speed = 1.0

        # Acceleration paramater controls y component change and controls visual appareance of 'speed' of bomb
        # Bomb will 'fall' faster for higher acceleration number
        self.acceleration = .009

        # As drag constant increases the distance bomb travels in x increases over time
        # This is inverse what you would expect from a drag constant
        self.drag = .03

        # Keep track of the time the ground explosion has occured using a counter
        self.ground_explosion_counter = 1
        # Keep track of the time the tank explosion has occured using a counter
        self.tank_explosion_counter = 1

        # I need a flag to determine if the bomb has collided with the ground or not
        # All bombs start in the air so this and the tank flag will initially be False until changed to True
        self.bomb_collided_with_ground = False
        # I need a flag to determine if the bomb has collided with a tank or not
        self.bomb_collided_with_tank = False
        # Becuase the ground collision check is a positional evaluation and because when I explode with either the
        # ground or the tank I am changing the y pos of the bomb, and because free fall runs when the bomb is not at the
        # ground level I need to be able to tell free fall the bomb should not fall - after hitting a tank or already
        # hitting the ground
        self.continue_falling = True

    def update(self, enemy_tanks):
        """Check if we've collided with the ground or with a tank if so draw explosions if not continue falling"""
        # Before I move the y pos I need to check if the bomb has collided with the ground or with a tank
        self._check_ground_collision()
        # I will pass in the enemy tanks group from my game so that I can use the sprite-collide function to check for
        # collisions and delete the tanks collided with
        self._check_tank_collision(enemy_tanks)
        # If the bomb did not hit the groud and did not hit a tank continue falling
        if not self.bomb_collided_with_ground and not self.bomb_collided_with_tank and self.continue_falling:
            self.rect.y += self.bomb_vertical_speed
            # Increase the rate at which we increase our vertical speed - giving the effect of acceleration which
            # simulates the effect of gravity
            self.bomb_vertical_speed += self.bomb_vertical_speed * 0.025
        # If the bomb hit the ground and not a tank then call the method that will turn the bomb into a ground explosion
        elif self.bomb_collided_with_ground and not self.bomb_collided_with_tank:
            self.explode_ground()
        # If the bomb did not hit the ground but hit a tank then call the method to turn the bomb into a tank explosion
        elif not self.bomb_collided_with_ground and self.bomb_collided_with_tank:
            self.explode_tank()
    def _check_ground_collision(self):
        """Check if the bomb hit the ground, if it did call explode function to turn bomb into an explosion"""
        # only evaluate the y pos of the bomb if the bomb has not exploded yet, becasue if it has already exploded
        # then I am no longer needing to evaluate its y position
        if not self.bomb_collided_with_ground:
            if self.rect.y >= self.settings.screen_height - self.settings.ground_height + 20 - self.rect.height:
                # If the bomb hits the ground the bomb no longer needs to fall so change continue falling flag
                # If the bomb hits the ground I need to pass that this occured by changing the bomb collided with ground
                # flag
                self.bomb_collided_with_ground = True
                self.continue_falling = False
        # If the bomb collided with the ground and its been on the screen for an alloted period of time - evaluated only
        # by how long it takes the counter to hit 15 - then kill the bomb and reset our counter
        elif self.bomb_collided_with_ground and self.ground_explosion_counter % 15 == 0:
                self.kill()
                # If we reset the counter to 0 then the expression above, self.ground_explosion_counter % 30 will always
                # be true because 0 % any integer == 0
                self.ground_explosion_counter = 1
        # If the bomb has exploded with the ground but hasnt been on the screen for the desired time yet then continue
        # to increment the counter
        elif self.bomb_collided_with_ground and not (self.ground_explosion_counter % 15 == 0):
            self.ground_explosion_counter += 1

    def _check_tank_collision(self, enemy_tanks):
        """Check if the bombs collided with enemy tanks, if so call explode"""
        # Kill the tank we explode with the sprite-collide function
        collision = pygame.sprite.spritecollide(self, enemy_tanks, True)
        # If there is a collision we need to make sure the bomb no longer falls by changing continue falling flag
        # Also need to pass that our bomb collided with tank flag is now true
        if collision:
            self.bomb_collided_with_tank = True
            self.continue_falling = False

    def explode_ground(self):
        """This will change the bomb to a new image of an explosion"""
        # Change the bomb image to the ground explosion image
        self.image = pygame.image.load('images/bomb_images/ground_bomb_explosion.png')
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect()
        self.rect.x = self.start_pos_x
        # Put the ground explosion on the ground
        self.rect.y = self.settings.screen_height - self.settings.ground_height + 20 - self.rect.height
    def explode_tank(self):
        """This will change the bomb to a new image of an explosion"""
        # Change the bomb image to the tank explosion image
        self.image = pygame.image.load('images/bomb_images/tank_or_missile_explosion.png')
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect()
        self.rect.x = self.start_pos_x
        # Set the explosion image on the ground
        self.rect.y = self.settings.screen_height - self.settings.ground_height + 20 - self.rect.height

    def draw_bomb(self):
        """Draw the bomb to the screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))