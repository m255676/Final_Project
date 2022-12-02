import pygame

class Settings():
    """Overall Game settings class"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.ground_height = self.screen_height / 10
        self.lives_left = 3
        self.score = 0
        self.high_score = 0
        self.game_level = 1
        self.bg_color = (215, 215, 215)

        # Points received for dropping a bomb on an enemy tank:
        self.tank_hit_points = 50
        self.score_multiplier = 1.25