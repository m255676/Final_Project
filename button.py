import pygame.font

class PlayButton:
    """ Class to manage the play button which will start the game play"""
    def __init__(self, jet_fighter_game, msg):
        """Initialize button attributes"""
        self.screen = jet_fighter_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 250, 50
        # Make the pause button color grey
        self.button_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Draw a blank button and then draw the message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class PauseButton:
    """ Class to manage the pause button which will pause the game"""
    def __init__(self, jet_fighter_game, msg):
        """Initialize button attributes"""
        self.screen = jet_fighter_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 80, 25
        # Make the pause button color grey
        self.button_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 26)

        # Build the button's rect and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # Set the button to the top left corner of the game so that its out of the way
        self.rect.x = 0
        self.rect.y = 0
        self.rect.topleft = (self.rect.x, self.rect.y)

        # The button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = (self.width/2, self.height/2)

    def draw_button(self):
        """ Draw a blank button and then draw the message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class PlayAgainButton:
    """ Class to manage the play button which will start the game play"""
    def __init__(self, jet_fighter_game, msg):
        """Initialize button attributes"""
        self.screen = jet_fighter_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 250, 50
        # Make the pause button color grey
        self.button_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Draw a blank button and then draw the message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)