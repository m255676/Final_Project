import pygame.font

class Scoreboard:
    """Class to report scoring information."""

    def __init__(self, jet_fighter_game):
        """Initialize scorekeeping attributes"""
        self.screen = jet_fighter_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = jet_fighter_game.settings
        self.stats = jet_fighter_game.stats

        # Font settings for scoring information.
        self.text_color = (250, 250, 250)
        self.bg_color = self.settings.bg_color
        self.font = pygame.font.SysFont(None, 32)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """Turn the score into a rendered image."""
        # The dynamic integer is turned into a string so we may render it and then display it in our scoreboard
        # Round the score
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        # Text that score will go under, reads "CURRENT SCORE:"
        score_txt = "CURRENT SCORE"
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
        self.high_score_txt_rect.x = self.score_txt_rect.x - self.high_score_txt_rect.width - 20
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

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()