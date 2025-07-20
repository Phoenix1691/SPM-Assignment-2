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
