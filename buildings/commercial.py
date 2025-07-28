# commercial.py - This file defines the Commercial building class for the city-building game.
'''
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
        
    def calculate_arcade_coins(self, adjacent_buildings):
        # Arcade mode: +1 coin per adjacent Residential (R)
        return adjacent_buildings.get("R", 0)


# 1 point per commercial, 1 point per residential
'''
from buildings.building_parent import Building

class commercial(Building):
    def __init__(self):
        super().__init__()
        self.type = "Commercial"
        self.size = (1, 1)
        self.color = (150, 200, 255)
        self.adjacency = {
            "I": 1
        }
        self.type_identifier = "C"
        self.profit = 3
        self.upkeep = 2

    def score(self, grid, row, col, mode="arcade", visited=None):
        if mode == "arcade":
            score = 0
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = grid.get((row + dy, col + dx))
                if neighbor:
                    if neighbor.type_identifier in ["R", "C"]:
                        score += 1
            return max(score, 0)
        elif mode == "freeplay":
            # Return zero or neutral score for freeplay mode
            return 0, 0
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")

    def calculate_profit_and_upkeep(self, grid, row, col, mode="freeplay"):
        if mode == "freeplay":
            return self.profit, self.upkeep
        elif mode == "arcade":
            return self.score(grid, row, col, mode)
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")
