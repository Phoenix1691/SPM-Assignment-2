# buildings/park.py - This file defines the Park building type in the city-building game.
from buildings.building_parent import Building

class park(Building):
    type_identifier = "O"

    def score(self, connected_counts):
        # Park: 1 point per connected park
        return connected_counts.get("O", 0)

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Park generates no profit, costs 1 coin upkeep
        return 0, 1