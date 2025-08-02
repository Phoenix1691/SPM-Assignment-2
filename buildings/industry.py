# industry.py - Industry building class for the city-building game
from buildings.building_parent import Building

class industry(Building):
    type_identifier = "I"

    def score(self, adjacent_counts):
        # 1 point per industry in the city (handled in calculate_score)
        # We'll return 1 here, and let total industries multiply
        return 1

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Industry generates 2 coins per turn
        profit = 2
        # Each industry costs 1 coin upkeep
        upkeep = 1
        # Extra profit: 1 coin per adjacent residential
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = grid.get((row+dr, col+dc))
            if neighbor and getattr(neighbor, "type_identifier", "") == "R":
                profit += 1
        return profit, upkeep
