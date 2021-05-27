class Settings:
    """Store all settings for game alien invasion"""

    def __init__(self) -> None:
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 30

        # alien settings
        self.fleet_drop_speed = 10

        # increse difficulty when level has up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ init settings, these values will change during the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.2

        # 1 -> move to the right, -1 -> move to the left
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        """those value will increase as the game proceed"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    