# commercial.py - This file defines the Commercial building class for the city-building game.
from buildings.building_parent import Building

class commercial (Building):
    def __init__(self):
        self.name = "Commercial Building"
        self.size = (1, 1)
        self.profit = 3
        self.upkeep = 2
        self.color = (0, 255, 0)  # Green color for commercial buildings
        self.type = "C"  # Type identifier for commercial buildings

# Commercial (C): Each commercial generates 3 coins per turn and cost 2 coins per turn to upkeep.
    def calculate_profit_and_upkeep(self, grid):
        profit = self.profit
        upkeep = self.upkeep
        # Additional logic for calculating profit and upkeep based on the grid can be added here
        return profit, upkeep

# Commercial (C): Scores 1 point per commercial adjacent to it. Each commercial generates 1 coin per residential adjacent to it.
    def score(self, adjacent_buildings):
        score = 0
        score += adjacent_buildings.get("C", 0)
        score += adjacent_buildings.get("R", 0)
        return score


# 1 point per commercial, 1 point per residential
