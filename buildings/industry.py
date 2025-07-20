# industry.py - Industry building class for the city-building game
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