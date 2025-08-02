# buildings/residential.py - This file defines the Residential building type in the city-building game.
# Residential (R): Scores 1 point per R or C, 2 points per O
from buildings.building_parent import Building

class residential(Building):
    type_identifier = "R"

    def score(self, connected_counts):
        # Score for residential:
        # - If any industry connected → 1 point total
        # - Else: 1 per R or C, 2 per O
        if connected_counts.get("I", 0) > 0:
            return 1
        return (
            connected_counts.get("R", 0)
            + connected_counts.get("C", 0)
            + connected_counts.get("O", 0) * 2
        )

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Base profit/upkeep:
        # - 1 coin profit
        # - 1 coin upkeep per contiguous R cluster (handled per building)
        profit = 1

        # Compute R cluster for upkeep cost
        visited = set()
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                neighbor = grid.get((r+dr, c+dc))
                if neighbor and getattr(neighbor, "type_identifier", "") == "R":
                    stack.append((r+dr, c+dc))

        upkeep = 1  # 1 coin per cluster
        return profit, upkeep
