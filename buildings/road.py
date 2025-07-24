# buildings/road.py - This file defines the Road building type in the city-building game.
# • Road (*): Scores 1 point per connected road (*) in the same row.
#Park (O): Each park costs 1 coin to upkeep.

from buildings.building_parent import Building

class road(Building):
    def __init__(self):
        self.type = "Road"
        self.size = (1, 1)
        self.color = (0, 0, 0)  # Black color for roads
        self.type_identifier = "*"
        self.upkeep = 1  # Upkeep for road segments
        self.adjacency = {
            "*": 1,  # Road
        }

# Road (*): Scores 1 point per connected road (*) in the same row.
    def score(self, adjacent_buildings):
        score = 0
        # Count the number of connected road segments in the same row
        for building_type, count in adjacent_buildings.items():
            if building_type == "*":
                score += count
        return score
    
# Road (*): Each unconnected road segment costs 1 coin to upkeep.
    def calculate_profit_and_upkeep(self, grid):
        profit = 0
        upkeep = 0
        clusters = []
        road_segments = []
        visited = set()
        return profit, upkeep