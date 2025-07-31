from scoring import ScoringSystem  # Adjust import path if needed

class GameEconomy:
    def __init__(self, map_reference, mode="arcade"):
        """
        Initialize the economy manager.
        :param map_reference: Reference to the game map (grid, buildings, etc.)
        :param mode: "arcade" or "freeplay"
        """
        self.mode = mode
        self.map = map_reference
        self.score_system = ScoringSystem(map_reference)
        self.score = 0
        self.coins = 16 if mode == "arcade" else float('inf')  # Arcade starts with 16 coins; Freeplay unlimited

    def place_building(self, pos, building_abbr):
        """
        Attempt to place a building and update economy.
        For arcade mode, deduct 1 coin on placement.
        Updates score based on scoring system.
        Returns (success, message)
        """
        if self.mode == "arcade" and self.coins < 1:
            return False, "Not enough coins to place building."

        # Placement should be done externally on the map before calling this or 
        # add a method here to handle map placement too if needed.

        if self.mode == "arcade":
            self.coins -= 1

        self.score += self.score_system.scoring_main(pos, building_abbr)
        return True, "Building placed."

    def get_status_arcade(self, pos, building_abbr):
        """
        For arcade mode:
        Place building, update coins and score.
        Calculate coins generated this turn by industry/commercial buildings.
        Return (remaining_coins, current_score, message)
        """
        success, msg = self.place_building(pos, building_abbr)
        if not success:
            return self.coins, self.score, msg

        coins_gained = self.score_system.coin_gen_arcade()
        self.coins += coins_gained

        return self.coins, self.score, "OK"

    def get_status_freeplay(self):
        """
        For freeplay mode:
        Return profit, upkeep, and score from the scoring system.
        Coins are unlimited, so no coin tracking here.
        """
        profit, upkeep = self.score_system.calculate_profit_and_upkeep()
        score = self.score_system.calculate_score()
        return profit, upkeep, score
