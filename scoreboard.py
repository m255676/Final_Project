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
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial scroe image.
        self.prep_score()

        def prep_score(self):
            """Turn the score into a rendered image."""
            score_str = str(self.stats.score)
            self.score_image = self.font.render(score_str, True, self.text_color, self.settings)
