# buildings/road.py - This file defines the Road building type in the city-building game.
# # • Road (*): Scores 1 point per connected road (*) in the same row.
# #Park (O): Each park costs 1 coin to upkeep.
from buildings.building_parent import Building

class road(Building):
    type_identifier = "*"

    def score(self, connected_counts):
        # Roads scored by rows in main game logic, 
        # not here. Return 0.
        return 0

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Roads generate no profit.
        # Unconnected single roads cost 1 coin to upkeep.
        has_neighbor = False
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = grid.get((row+dr, col+dc))
            if neighbor and getattr(neighbor, "type_identifier", "") == "*":
                has_neighbor = True
                break
        return 0, 0 if has_neighbor else 1






