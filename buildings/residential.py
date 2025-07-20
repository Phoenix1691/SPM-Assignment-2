from buildings.building_parent import Building

class residential(Building):
    def __init__(self):
        self.type = "Residential"
        self.size = (1, 1)
        self.color = (255, 0, 0)  # Red color for residential buildings
        self.adjacency = {
            "I": 1,  # Industry
            "C": 1,  # Commercial
            "O": 2   # Park
        }
        self.type_identifier = "R"
        self.profit = 1
        self.upkeep = 1 # Upkeep for residential buildings cluster
# Residential (R): Each residential building generates 1 coin per turn. 
# Each cluster of residential buildings (must be immediately next to each other) requires 1 coin per turn to upkeep
    def calculate_profit_and_upkeep(self, grid):
        profit = self.profit
        upkeep = self.upkeep
        # Additional logic for calculating profit and upkeep based on the grid can be added here
        return profit, upkeep
    
    def score(self, adjacent_buildings):
        score = 0
        if "I" in adjacent_buildings:
            score += 1
        else:
            score += adjacent_buildings.get("R", 0) + adjacent_buildings.get("C", 0)
            score += 2 * adjacent_buildings.get("O", 0)
        return score
#Residential (R): If it is next to an industry (I), then it scores 1 point only. 
# Otherwise, it scores 1 point for each adjacent residential (R) or commercial (C), and 2 points for each adjacent park (O).