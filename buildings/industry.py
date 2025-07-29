# industry.py - Industry building class for the city-building game
'''
from buildings.building_parent import Building

class industry(Building):
    def __init__(self):
        self.type = "Industry"
        self.size = (1, 1)
        self.color = (128, 128, 128)  # Gray color for industry buildings
        self.adjacency = {
            "R": 1,  # Residential
        }
        self.type_identifier = "I"
        self.profit = 2
        self.upkeep = 1

# Industry (I): Each industry generates 2 coins per turn and cost 1 coin per turn to upkeep.
    def calculate_profit_and_upkeep(self, grid):
        profit = self.profit
        upkeep = self.upkeep
        # Additional logic for calculating profit and upkeep based on the grid can be added here
        return profit, upkeep
    
# Industry (I): Scores 1 point per industry in the city. Each industry generates 1 coin per residential building adjacent to it.
    def score(self, adjacent_buildings):
        score = 0
        # Industry scores based on adjacent residential buildings
        score += adjacent_buildings.get("R", 0)
        return score
'''
from buildings.building_parent import Building

class industry(Building):
    def __init__(self):
        super().__init__()
        self.type = "Industry"
        self.size = (1, 1)
        self.color = (200, 200, 100)
        self.adjacency = {
            "R": -1,
            "C": 1,
            "*": 1
        }
        self.type_identifier = "I"
        self.profit = 2
        self.upkeep = 1

    def score(self, grid, row, col, mode="freeplay", visited=None):
        if mode == "arcade":
            score = 0
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = grid.get((row + dy, col + dx))
                if neighbor:
                    if neighbor.type_identifier == "C":
                        score += 1
                    elif neighbor.type_identifier == "*":
                        score += 1
                    elif neighbor.type_identifier == "R":
                        score -= 1
            return max(score, 0)
        elif mode == "freeplay":
            return self.profit, self.upkeep
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")

    def calculate_profit_and_upkeep(self, grid, row, col, mode="freeplay", visited=None):
        if mode == "freeplay":
            return self.profit, self.upkeep
        elif mode == "arcade":
            return self.score(grid, row, col, mode), 0
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")
