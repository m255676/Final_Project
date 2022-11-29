class GameStats:
    """Track statistics for Jet Fighter Game"""

    def __init__(self, jet_fighter_game):
        """Initialize statistics"""
        self.settings = jet_fighter_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.lives_left