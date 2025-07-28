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
        self.type = "Road"
        self.size = (1, 1)
        self.color = (0, 0, 0)  # Black color for roads
        self.type_identifier = "*"
        self.upkeep = 1  # Upkeep cost per disconnected cluster
        self.adjacency = {
            "*": 1,
        }

    def score(self, adjacent_buildings):
        # Arcade mode scoring: count connected road segments in the same row (adjacent left/right)
        return adjacent_buildings.get("*", 0)

    def calculate_profit_and_upkeep(self, grid, mode="freeplay"):
        profit = 0
        upkeep = 0

        if mode == "freeplay":
            # Find all clusters of connected roads (adjacent in 4 directions)
            visited = set()
            clusters = 0

            def neighbors(r, c):
                for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                        yield nr, nc

            for r in range(len(grid)):
                for c in range(len(grid[0])):
                    if grid[r][c] and grid[r][c].type_identifier == "*" and (r, c) not in visited:
                        # BFS or DFS to find cluster
                        stack = [(r,c)]
                        visited.add((r,c))
                        while stack:
                            rr, cc = stack.pop()
                            for nr, nc in neighbors(rr, cc):
                                if (nr, nc) not in visited and grid[nr][nc] and grid[nr][nc].type_identifier == "*":
                                    visited.add((nr, nc))
                                    stack.append((nr, nc))
                        clusters += 1

            upkeep = clusters * self.upkeep

        elif mode == "arcade":
            upkeep = 0  # No upkeep in arcade mode

        return profit, upkeep
