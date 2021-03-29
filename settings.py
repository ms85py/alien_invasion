
class Settings:
    def __init__(self):
        # screen settings
        self.screen_width = 1550
        self.screen_height = 1000
        self.bg_color = (0, 0, 0)

        # ship stuff
        self.ship_limit = 3

        # bullet stuff
        self.bullet_width = 6
        self.bullet_height = 18
        self.bullet_color = (255, 255, 255)
        self.bullets_max = 3

        # alien stuff
        self.fleet_drop_speed = 30

        # game speed up scale
        self.speedup_scale = 1.1

        # scoring scale strength
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """initializes settings that'll change while playing"""
        self.ship_speed = 0.75
        self.bullet_speed = 0.7
        self.alien_speed = 0.25
        # 1 = to the right, -1 = to the left
        self.fleet_direction = 1

        # points for each alien ship shot down
        self.alien_points = 50


    def increase_speed(self):
        """increases game speed and alien score"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

