import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """This class manages missiles shot by enemy jet"""
    # Pass in the Sprite Class to access its featuress

    def __init__(self, enemy_jet):
        """Create a missile at the enemy jets current location"""
        super().__init__()
        self.screen = enemy_jet.screen

        self.image = pygame.image.load('images/bomb_images/tank_or_missile_explosion.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

        self.rect.x = enemy_jet.rect.x
        self.rect.y = enemy_jet.rect.y

        # This is the counter that will determine the time the explosion spends on the screen
        self.life_lived = 1

    def lifespan(self):
        """Run a counter to kill self"""
        if self.life_lived % 15 == 0:
            self.kill()
            print("Kill Explosion")
            print(f"x: {self.rect.x}")
            print(f"y: {self.rect.y}")
        else:
            # If we haven't hit the timer then continue to increment the timer
            self.life_lived += 1
    def update(self):
        """ Call the lifespan function"""
        self.lifespan()
    def draw_explosion(self):
        """Draw the explosion to the screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))