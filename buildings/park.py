# buildings/residential.py - Residential building class for the city-building game
from buildings.building_parent import Building

class park(Building):
    type_identifier = "O"

    def score(self, adjacent_counts):
        # 1 point per adjacent park
        return adjacent_counts.get("O", 0)

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Parks generate no profit, cost 1 upkeep
        return 0, 1
