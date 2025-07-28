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
        self.name = "Commercial Building"
        self.size = (1, 1)
        self.profit = 3       # Freeplay: base profit
        self.upkeep = 2       # Freeplay: upkeep cost
        self.color = (0, 255, 0)  # Green color for commercial buildings
        self.type_identifier = "C"  # Type identifier for commercial buildings

    # Freeplay profit and upkeep calculation
    def calculate_profit_and_upkeep(self, mode="freeplay", adjacent_buildings=None):
        if mode == "freeplay":
            profit = self.profit
            upkeep = self.upkeep
        elif mode == "arcade":
            # In arcade, profit depends on adjacent Residential (R)
            profit = adjacent_buildings.get("R", 0) if adjacent_buildings else 0
            upkeep = 0  # No upkeep in arcade
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")
        return profit, upkeep

    # Scoring based on adjacency (for both modes, per specs)
    def score(self, adjacent_buildings):
        score = 0
        score += adjacent_buildings.get("C", 0)  # 1 point per adjacent Commercial
        score += adjacent_buildings.get("R", 0)  # 1 point per adjacent Residential
        return score

