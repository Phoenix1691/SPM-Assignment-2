# buildings/residential.py - Residential building class for the city-building game
'''
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
'''
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
        self.upkeep = 1  # Upkeep per cluster of connected residential buildings

    def calculate_profit_and_upkeep(self, grid, mode="freeplay"):
        """
        Calculate profit and upkeep for freeplay or arcade.
        In arcade mode: no base profit or upkeep from residential.
        In freeplay mode: base profit per building, upkeep per cluster.
        """
        if mode == "arcade":
            return 0, 0  # No base profit or upkeep in arcade mode

        # Freeplay logic - calculate clusters and profit
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        visited = set()

        def neighbors(r, c):
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    yield nr, nc

        total_buildings = 0
        clusters = 0

        for r in range(rows):
            for c in range(cols):
                building = grid[r][c]
                if building and building.type_identifier == "R" and (r, c) not in visited:
                    stack = [(r, c)]
                    visited.add((r, c))
                    total_buildings += 1
                    while stack:
                        rr, cc = stack.pop()
                        for nr, nc in neighbors(rr, cc):
                            neighbor_building = grid[nr][nc]
                            if (nr, nc) not in visited and neighbor_building and neighbor_building.type_identifier == "R":
                                visited.add((nr, nc))
                                stack.append((nr, nc))
                                total_buildings += 1
                    clusters += 1

        profit = total_buildings * self.profit
        upkeep = clusters * self.upkeep

        return profit, upkeep

    def score(self, adjacent_buildings):
        """
        Residential scoring rules:
        - If next to Industry (I), scores 1 point only.
        - Otherwise, scores 1 point per adjacent Residential (R) or Commercial (C),
          and 2 points per adjacent Park (O).
        """
        if "I" in adjacent_buildings and adjacent_buildings["I"] > 0:
            return 1
        return adjacent_buildings.get("R", 0) + adjacent_buildings.get("C", 0) + 2 * adjacent_buildings.get("O", 0)
