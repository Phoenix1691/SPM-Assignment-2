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
        super().__init__()
        self.type = "Residential"
        self.size = (1, 1)
        self.color = (255, 0, 0)
        self.adjacency = {
            "I": 1,
            "C": 1,
            "O": 2
        }
        self.type_identifier = "R"
        self.profit = 1
        self.upkeep = 1

    def score(self, grid, row, col, mode="arcade", visited=None):
        if mode == "arcade":
            score = 0
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = grid.get((row + dy, col + dx))
                if neighbor:
                    if neighbor.type_identifier == "C":
                        score += 1
                    elif neighbor.type_identifier == "I":
                        score -= 1
            return max(score, 0)

        elif mode == "freeplay":
            if visited is None:
                visited = set()

            if (row, col) in visited:
                return 0  # Already counted

            cluster = set()
            stack = [(row, col)]
            while stack:
                r, c = stack.pop()
                if (r, c) in visited or (r, c) in cluster:
                    continue
                building = grid.get((r, c))
                if building and building.type_identifier == "R":
                    cluster.add((r, c))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if (nr, nc) not in cluster and grid.get((nr, nc)) and grid[(nr, nc)].type_identifier == "R":
                            stack.append((nr, nc))

            visited.update(cluster)
            return len(cluster)  # return profit only

        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")

    def calculate_profit_and_upkeep(self, grid, row, col, mode="freeplay", visited=None):
        if mode == "freeplay":
            if visited is None:
                visited = set()
            profit = self.score(grid, row, col, mode="freeplay", visited=visited)
            upkeep = self.upkeep if profit > 0 else 0
            return profit, upkeep
        elif mode == "arcade":
            profit = self.score(grid, row, col, mode="arcade")
            return profit, 0
        else:
            raise ValueError("Mode must be 'freeplay' or 'arcade'")


