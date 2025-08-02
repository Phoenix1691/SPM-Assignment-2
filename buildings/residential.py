# buildings/residential.py - Residential building class for the city-building game
from buildings.building_parent import Building

class residential(Building):
    type_identifier = "R"

    def score(self, adjacent_counts):
        # Adjacent to industry → always 1 point
        if adjacent_counts.get("I", 0) > 0:
            return 1
        # 1 point per adjacent R or C, 2 points per adjacent O
        return (
            adjacent_counts.get("R", 0)
            + adjacent_counts.get("C", 0)
            + adjacent_counts.get("O", 0) * 2
        )

    def calculate_profit_and_upkeep(self, grid, row, col, mode=None):
        # Generates 1 coin per turn
        profit = 1
        # Determine cluster size for upkeep cost
        # Cluster = contiguous Rs (4-directional)
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
