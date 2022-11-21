import pygame

class Ground:
    """This is our ground surface"""
    def __init__(self, jet_fighter_game):
        # Pass in the jet fighter game so that the settings/ sizing of ground is all proportional/ relative
        self.settings = jet_fighter_game.settings
        self.rect_width = jet_fighter_game.settings.screen_width
        self.rect_height = jet_fighter_game.settings.ground_height
        self.rect = pygame.Rect((0, jet_fighter_game.settings.screen_height - self.rect_height),(self.rect_width, self.rect_height))
        # Need to pass this in to draw the ground to the screen:
        self.screen = jet_fighter_game.screen
        self.color = (93, 179, 84)
    def draw_ground(self):
        """This draws the ground"""
        pygame.draw.rect(self.screen, self.color, self.rect)