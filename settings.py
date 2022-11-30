import pygame

class Settings():
    """Overall Game settings class"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.ground_height = self.screen_height / 10
        self.lives_left = 1
        self.score = 0
        self.bg_color = (215, 215, 215)