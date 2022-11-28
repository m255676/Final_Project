import pygame

class Ground:
    """This is our ground surface"""
    def __init__(self, jet_fighter_game):
        # Pass in the jet fighter game so that the settings/ sizing of ground is all proportional/ relative
        self.settings = jet_fighter_game.settings
        self.image = pygame.image.load('images/ground_terrain_2_cropped.bmp.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (jet_fighter_game.settings.screen_width, jet_fighter_game.settings.screen_height/8))
        self.rect = self.image.get_rect()
        # Need to pass this in to draw the ground to the screen:
        self.screen = jet_fighter_game.screen
        self.rect.y = jet_fighter_game.settings.screen_height - jet_fighter_game.settings.screen_height/10
        self.rect.x = 0
    def blitme(self):
        """This is what will allow the jet to be drawn to the screen when we call from jet fighter game"""
        self.screen.blit(self.image, (self.rect.x,self.rect.y))