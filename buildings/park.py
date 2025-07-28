# buildings/residential.py - Residential building class for the city-building game
'''
from buildings.building_parent import Building

class park(Building):
    def __init__(self):
        self.type = "Park"
        self.size = (1, 1)
        self.color = (0, 255, 0)  # Green color for park buildings
        self.type_identifier = "O"
        self.upkeep = 1
        self.adjacency = {
            "O": 1,  # Park
        }

# Park (O): Each park costs 1 coin to upkeep.
    def calculate_profit_and_upkeep(self, grid):
        profit = 0
        upkeep = self.upkeep
        # Additional logic for calculating profit and upkeep based on the grid can be added here
        return profit, upkeep
    
# Park (O): Scores 1 point per park adjacent to it.
    def score(self, adjacent_buildings):
        score = 0
        # Parks score based on adjacency to other parks
        score += adjacent_buildings.get("O", 0)
        return score
'''
from buildings.building_parent import Building

class park(Building):
    def __init__(self):
        super().__init__()
        self.type = "Park"
        self.size = (1, 1)
        self.color = (0, 255, 0)
        self.type_identifier = "O"
        self.upkeep = 1

    def get_adjacent_buildings_counts(self, grid, row, col):
        counts = {}
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = grid.get((row + dy, col + dx))
            if neighbor:
                key = getattr(neighbor, "type_identifier", None)
                if key:
                    counts[key] = counts.get(key, 0) + 1
        return counts

    def score(self, grid, row, col, mode="freeplay", visited=None):
        if mode == "arcade":
            count = 0
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = grid.get((row + dy, col + dx))
                if neighbor and neighbor.type_identifier == "O":
                    count += 1
            return count, 0
        elif mode == "freeplay":
            return 0, self.upkeep
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")

    def calculate_profit_and_upkeep(self, grid, row, col, mode="freeplay"):
        profit, upkeep = self.score(grid, row, col, mode)
        return profit, upkeep
