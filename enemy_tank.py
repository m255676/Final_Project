import pygame
from pygame.sprite import Sprite

class Enemy_Tank(Sprite):
    """Overall class to manage enemy tank attributes and actions"""
    def __init__(self, jet_fighter_game):
        """Initialize enemy tank by passing in screen dimensions used in game"""
        super().__init__()
        self.screen = jet_fighter_game.screen
        self.screen_width = jet_fighter_game.settings.screen_width
        self.screen_height = jet_fighter_game.settings.screen_height
        self.screen_rect = jet_fighter_game.screen.get_rect()

        self.image = pygame.image.load('images/tank_images/American_sherman_attack_1.bmp').convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (70,70))
        # Still need to mirror tank so that its orriented the right direction

        self.rect = self.image.get_rect()

        self.start_pos_x = self.screen_width - self.rect.width
        self.start_pos_y = self.screen_height - jet_fighter_game.ground.rect.height - 15
        self.rect.x = self.start_pos_x

        self.tank_speed = 1.50

    def update(self, time):
        """Move Tanks"""
        self.move_tank(time)
        #collision = pygame.sprite.spritecollide(self, bombs, True)

    def move_tank(self, time):
        """Function to move tank"""
        self.rect.x -= self.tank_speed
        self.rect.y = self.start_pos_y
        # Creating this Rect attribute so collision will run
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        # Over time speed up the tank speed but max it out at a speed that makes game play relatively difficult
        if (time % 500) == 0:
            if self.tank_speed >= 3.0:
                self.tank_speed = 3.0
            else:
                # Scale up the tank speed by some amount after every so ofter
                self.tank_speed += 0.25
    def draw_tank(self):
        """Function to draw tank to screen"""
        self.screen.blit(self.image, self.rect)