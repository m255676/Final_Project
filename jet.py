import pygame
from pygame.sprite import Sprite
from time import sleep

class Jet:
    """Class to manage Jet gameplay"""
    def __init__(self, jet_fighter_game):
        """Initialize the jet and set its starting position"""
        # Pass in the screen dimensions from jet fighter game
        self.screen = jet_fighter_game.screen
        self.settings = jet_fighter_game.settings
        self.scoreboard = jet_fighter_game.scoreboard
        self.stats = jet_fighter_game.stats
        self.score_multiplier = jet_fighter_game.score_multiplier

        # Use the get_rect() method so we can access the screen dimensions and use them later
        self.screen_rect = jet_fighter_game.screen.get_rect()

        # Load the jet's image
        self.image = pygame.image.load('images/jet_images/AEG_CIV_attack_1.bmp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,60))
        # Get the Jet's Rect so we can access and work with its dimmensions later
        self.rect = self.image.get_rect()
        self.height = self.rect.height

        # Store a decimal value for the jet's horizontal position
        self.x = float(self.rect.x)
        # Store a decimal value for the jet's vertical position
        self.y = float(self.rect.y)

        # Flags that will be changed in keydown/ups in order to have continous movement for duration of keydown
        self.moving_up = False
        self.moving_down = False
        self.speeding_up = False

        # This controls how fast our jet moves across the screen
        self.jet_speed_x = 3.0
        self.acceleration = .005

    def _check_lives(self):
        """Function that checks the lives left and changes the image of the jet accordingly"""
        if self.settings.lives_left == 3:
            # Load the jets original image
            self.image = pygame.image.load('images/jet_images/AEG_CIV_attack_1.bmp').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
        if self.settings.lives_left == 2:
            # Load the jet's new image
            self.image = pygame.image.load('images/jet_images/Damaged_Jet_1_Transparent.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
        elif self.settings.lives_left == 1:
            # Load the jet's new image
            self.image = pygame.image.load('images/jet_images/Damaged_Jet_2_Transparent.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (55, 55))
        elif self.settings.lives_left == 0:
            # Load the jet's new image
            self.image = pygame.image.load('images/jet_images/AEG_CIV_death_1.png').convert_alpha()
            # This image appears to be scaled differently so I'm making it larger so that the observable
            # jet size is consistent
            self.image = pygame.transform.scale(self.image, (70, 70))

    def move_jet(self, enemy_missiles, bombs, tanks, counter):
        """Ques the horizontal and vertical movements, so they happen nearly simultaneously"""
        # Check lives left and adjust image based on lives left
        self._check_lives()
        # Check if we have collided with any enemy missiles, if so then delete the enemy missile
        missile_jet_collision = pygame.sprite.spritecollide(self, enemy_missiles, True)
        if missile_jet_collision:
            # Subtract one life from the number of lives left if an enemy missile hit us
            # check lives above will set the plane's image depending on how many lives we have left
            self.settings.lives_left -= 1
        # I am not going to delete the tanks or bombs here, I will do that in the bomb instance when it uses
        # spritecollideany. I just want to evaluate a collision between bombs and tanks so I know to add to the score
        bomb_tank_collision = pygame.sprite.groupcollide(bombs, tanks, False, False)
        if bomb_tank_collision:
            # When the bombs and tanks collide add the respective points to the score
            # Then display this score by 'preping' the score and high score
            self.stats.score += self.settings.tank_hit_points
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()

        # Move the jet to the right
        self.fly_right()
        # Call increase or decrease functions which will run when their flags are set true- when the player moves
        # the plane up or down using the arrow keys
        self.increase_altitude()
        self.decrease_altitude()
        # Increase the value added to the score at the same rate the levels change so that the further in the game you
        # advance the more you can score
        if (counter % 500 * 10) == 0:
            self.settings.tank_hit_points = self.settings.tank_hit_points * self.score_multiplier

    def fly_right(self):
        """Method that will move the jet rightward on the screen"""
        # Check if the jet is at the right edge, if it is reset to the left side before flying right
        if self.rect.x > self.settings.screen_width:
            self._reset_jet()
            # After we reset the jet also reset our bombs and missiles available
            self.settings.bombs_available = 4
            self.settings.friendly_missiles_available = 3

        if self.speeding_up:
            self.jet_speed_x = 7
            self.rect.x += self.jet_speed_x
        else:
            self.jet_speed_x = 3.0
            self.rect.x += self.jet_speed_x
    def increase_altitude(self):
        """This will increase the altitude of the jet"""
        # Only increase altitude when not at top of screen
        jet_speed_up = 4.25 #Later move to settings
        if self.rect.y > 0 and self.moving_up:
            self.rect.y -= jet_speed_up

    def decrease_altitude(self):
        """This will decrease the altitude of the jet"""
        # Only decrease if not below bottom third of screen
        jet_speed_down = 4.25 #Later move to settings
        if self.rect.y < self.settings.screen_height * 2/3 and self.moving_down:
            self.rect.y += jet_speed_down

    def _reset_jet(self):
        """Method to return the jet to the left of the screen"""
        # Jet is actually drawn in the negative x to give it a smoother effect of coming out of the left margin
        self.rect.x = 0 - self.rect.width

    def blitme(self):
        """This is what will allow the jet to be drawn to the screen when we call from jet fighter game"""
        self.screen.blit(self.image, self.rect)