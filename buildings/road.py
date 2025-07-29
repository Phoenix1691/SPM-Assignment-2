# buildings/road.py - This file defines the Road building type in the city-building game.
# • Road (*): Scores 1 point per connected road (*) in the same row.
#Park (O): Each park costs 1 coin to upkeep.
'''
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
'''
from buildings.building_parent import Building

class road(Building):
    def __init__(self):
        super().__init__()
        self.type = "Road"
        self.size = (1, 1)
        self.color = (0, 0, 0)
        self.type_identifier = "*"
        self.adjacency = {
            "*": 1,
        }
        self.profit = 0
        self.upkeep = 1

    def score(self, grid, row, col, mode="arcade", visited=None):
        if mode == "arcade":
            count = 0
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = grid.get((row + dy, col + dx))
                if neighbor and neighbor.type_identifier == "*":
                    count += 1
            return count  # return just the score
        elif mode == "freeplay":
            return 0  # roads don't score in freeplay
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")

    def calculate_profit_and_upkeep(self, grid, row, col, mode, visited=None):
        if mode == "freeplay":
            # your existing freeplay logic here
            connected = False
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = grid.get((row + dy, col + dx))
                if neighbor and neighbor.type_identifier in ("*", "R"):
                    connected = True
                    break

            upkeep = 0 if connected else 1
            profit = 0
            return profit, upkeep
            upkeep = 0 if connected else 1
            profit = 0
            return profit, upkeep

        elif mode == "arcade":
            # For arcade mode, define how roads affect scoring or coins
            # For example, return the count of adjacent roads as profit, upkeep 0:
            count = 0
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = grid.get((row + dy, col + dx))
                if neighbor and neighbor.type_identifier == "*":
                    count += 1
            return count, 0

        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")





