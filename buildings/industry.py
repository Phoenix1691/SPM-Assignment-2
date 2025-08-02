# buildings/industry.py - This file defines the Industry building type in the city-building game.
from buildings.building_parent import Building

class industry(Building):
    type_identifier = "I"

    def score(self, connected_counts):
        # Industry scores 1 point per industry in the city.
        # (Handled per building for simplicity.)
        return connected_counts.get("I", 0)

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Base profit/upkeep for Industry:
        # - Generates 2 coins per turn
        # - Costs 1 coin upkeep
        # - Extra profit per connected Residential handled centrally
        return 2, 1