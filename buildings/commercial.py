# buildings/commercial.py - This file defines the Commercial building type in the city-building game.
from buildings.building_parent import Building

class commercial(Building):
    type_identifier = "C"

    def score(self, connected_counts):
        # Commercial: 1 point per adjacent commercial
        return connected_counts.get("C", 0)

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Base profit/upkeep for Commercial:
        # - Generates 3 coins per turn
        # - Costs 2 coins upkeep
        # - Extra profit per connected Residential handled centrally
        return 3, 2
