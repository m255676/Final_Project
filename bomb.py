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
        #self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()

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
        # Redefining self.rect input here using pygame.Rect so spritecollideany function will work
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)


        # This will be the duration of time for the ground bomb explosion to occur
        self.bomb_ground_explosion_length = 50
        # Need to keep track of if bomb has hit ground and if it is already exploding
        # Will do this by having a flag initally set to false and changed to true when it hits ground
        self.exploded_with_ground = False
        self.explosion_counter = 0

    def free_fall(self, explosion_counter):
        """Update the self.rect.x and y to create free fall effect"""
        # Only move the bomb if it has not collided with the ground
        # if the bomb has already started to explode let it finish off
        if self.exploded_with_ground:
            pass
            if explosion_counter % 30 == 0:
                self.kill()
                # Reset our explosion counter so every bomb gets the same length of time on the screen
                self.explosion_counter = 0
        # if the bomb has exploded then continue to display it as an explosion at its respective position
        # when it collided with the ground until its killed
        elif self.exploded_with_ground:
            self.explode()
        # If the bomb has not hit the ground yet continue to fall
        elif not self.exploded_with_ground:
            self.rect.y += self.bomb_vertical_speed
            # Bomb vertical speed will increment exponentially - giving the effect of gravity
            self.bomb_vertical_speed += self.bomb_vertical_speed * .025

    def explode(self):
        """This will change the bomb to a new image of an explosion"""
        self.image = pygame.image.load('images/bomb_images/ground_bomb_explosion.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = self.start_pos_x
        self.rect.y = self.settings.screen_height - self.settings.ground_height + 45 - self.rect.height
    def _check_ground_collision(self):
        """Insert Explosion image if bomb hits ground and delete bomb"""
        # Threw in arbitrary number at end of equation to try and account for tanks being offset on ground for a
        # more pleasing 3d effect
        if self.rect.y >= self.settings.screen_height - self.settings.ground_height + 20 - self.rect.height:
            # If the bomb hits the ground I want its y position to stay here so that it remains on the ground for
            # the duration of its explosion
            self.rect.y = self.settings.screen_height - self.settings.ground_height + 20 - self.rect.height
            self.exploded_with_ground = True
            self.explode()

        else:
            self.exploded_with_ground = False
    def update(self):
        """Call Fall and Check Ground or Tank Collisions"""
        # Check ground collision before free-falling so that we know if the bomb should continue falling or not
        self._check_ground_collision()
        # Also increment the explosion counter before free falling
        # This counter will be used to cue the self.kill() after the explosion has been on the screen for a goal time
        self.explosion_counter += 1
        self.free_fall(self.explosion_counter)

    def draw_bomb(self):
        """Draw the bomb to the screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))