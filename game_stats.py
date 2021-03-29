
class GameStats:
    """tracks statistics"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        # starts the game in inactive state
        self.game_active = False

        # high score - doesn't reset
        self.high_score = 0


    def reset_stats(self):
        """reset/initialize stats"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

