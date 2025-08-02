# commercial.py - This file defines the Commercial building class for the city-building game.

from buildings.building_parent import Building

class commercial(Building):
    type_identifier = "C"

    def score(self, adjacent_counts):
        # 1 point per adjacent commercial
        return adjacent_counts.get("C", 0)

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        profit = 3  # per turn
        upkeep = 2
        # Extra profit: 1 coin per adjacent residential
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = grid.get((row+dr, col+dc))
            if neighbor and getattr(neighbor, "type_identifier", "") == "R":
                profit += 1
        return profit, upkeep
