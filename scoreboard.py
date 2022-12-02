import pygame.font
from pygame.sprite import Group
from jet import Jet

class Scoreboard:
    """Class to report scoring information: Level, High Score, Current Score"""

    def __init__(self, jet_fighter_game):
        """Initialize scorekeeping attributes"""
        self.jet_fighter_game = jet_fighter_game
        self.screen = jet_fighter_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = jet_fighter_game.settings
        self.stats = jet_fighter_game.stats

        # Font settings for scoring information.
        self.text_color = (250, 250, 250)
        self.bg_color = self.settings.bg_color
        self.font = pygame.font.SysFont(None, 32)

        # Prepare the initial score image and the current level image
        self.prep_score()
        self.prep_high_score()
        self.prep_game_level()
        self.prep_lives_left()

    def prep_lives_left(self):
        """Show how many lives are left"""
        # Make an empty sprite group that will house a jet for each number of lives the player has left
        # Then we will set each jet's position and then draw the group to the screen
        self.jets_left = Group()
        for jet_number in range(self.settings.lives_left):
            jet = Jet(self.jet_fighter_game)
            # Pause button is 80 pixels wide - I need to offset that distance plus account for the spacing of each jet
            # in order to display the next jet until all the jets are placed for each life left
            # This is why this is in a for loop, so that I can offset each jet relative to its place in lives left:
            jet.rect.x = 80 + 30 + jet_number * jet.rect.width
            jet.rect.y = 10
            self.jets_left.add(jet)

    def prep_game_level(self):
        """Turn the game level into a rendered image."""
        # The dynamic integer is turned into a string so we may render it and then display it in our scoreboard
        game_level_str = "{:,}".format(self.settings.game_level)
        self.game_level_image = self.font.render(game_level_str, True, self.text_color, None)

        # Text that game level will go under, reads "CURRENT LEVEL"
        game_level_txt = "LEVEL"
        self.game_level_txt_image = self.font.render(game_level_txt, True, self.text_color, None)

        # Display the score at the top right of the screen underneath the lettering "CURRENT SCORE".
        self.game_level_rect = self.game_level_image.get_rect()
        self.game_level_txt_rect = self.game_level_txt_image.get_rect()

        # Set the location of the score text and the score itself
        # Location needs to just offset from high score since high score is to its right on the screen - offset 20 pixel
        self.game_level_txt_rect.right = self.high_score_txt_rect.x - 30

        # Center under game level text
        self.game_level_rect.x = self.game_level_txt_rect.x + self.game_level_txt_rect.width/2

        self.game_level_rect.y = self.game_level_txt_rect.height + 5

    def prep_score(self):
        """Turn the score into a rendered image."""
        # The dynamic integer is turned into a string so we may render it and then display it in our scoreboard
        # Round the score
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        # Text that score will go under, reads "CURRENT SCORE:"
        score_txt = "SCORE"
        self.score_txt_image = self.font.render(score_txt, True, self.text_color, None)

        # Display the score at the top right of the screen underneath the lettering "CURRENT SCORE".
        self.score_rect = self.score_image.get_rect()
        self.score_txt_rect = self.score_txt_image.get_rect()

        # Set the location of the score text and the score itself
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.score_txt_rect.height + 5

        self.score_txt_rect.right = self.screen_rect.right - 20
        self.score_txt_rect.top = 0

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        # Make text that displays: "HIGH SCORE" above the high score value
        high_score_txt = "HIGH SCORE"
        self.high_score_txt_image = self.font.render(high_score_txt, True, self.text_color, None)

        # Have "high score" set 20 pixels to the left of current score, even in height with the text of "current score"
        self.high_score_txt_rect = self.high_score_txt_image.get_rect()
        self.high_score_txt_rect.x = self.score_txt_rect.x - self.high_score_txt_rect.width - 30
        self.high_score_txt_rect.top = self.score_txt_rect.top

        # Make the high score a string then make that string an image
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, None)

        # Have the high score centered under "HIGH SCORE"
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.high_score_txt_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw the score to the screen"""
        # Draw "Current Score" and score underneath it
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_txt_image, self.score_txt_rect)

        # Draw "High Score" and the high score underneath it
        self.screen.blit(self.high_score_txt_image, self.high_score_txt_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # Draw "Current Level" and level underneath it
        self.screen.blit(self.game_level_txt_image, self.game_level_txt_rect)
        self.screen.blit(self.game_level_image, self.game_level_rect)

        # Draw the jets/lives left
        # Because jets left is a sprite group I can use the draw method
        self.jets_left.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()