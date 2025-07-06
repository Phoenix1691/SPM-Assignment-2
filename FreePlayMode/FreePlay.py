# FreePlay.py - Main entry point for the Free Play mode
import pygame
import sys
import random

# Constants
BUILDING_TYPES = ["R", "I", "C", "O", "*"]

class FreePlayGame:
    def __init__(self):
        self.grid = self.create_grid(5)
        self.turn = 1
        self.loss_turns = 0
        self.max_loss_turns = 20
        self.coins = 1000  # Starting coins for display only, treated as unlimited
        self.score = 0     # Total score for the city

    def create_grid(self, size):
        return [["." for _ in range(size)] for _ in range(size)]

    def expand_grid_if_on_border(self, x, y, expansion_size=5):
        grid_size = len(self.grid)
        if x == 0 or y == 0 or x == grid_size - 1 or y == grid_size - 1:
            new_size = grid_size + 2 * expansion_size
            new_grid = self.create_grid(new_size)
            offset = expansion_size

            for old_y in range(grid_size):
                for old_x in range(grid_size):
                    new_grid[old_y + offset][old_x + offset] = self.grid[old_y][old_x]

            self.grid = new_grid
            return x + offset, y + offset
        return x, y

    def place_building(self, building, x, y):
        x, y = self.expand_grid_if_on_border(x, y)
        if self.grid[y][x] == ".":
            self.grid[y][x] = building
            # Deduct cost (always 1 coin) but do NOT block building if coins low
            self.coins -= 1  
            return True
        else:
            print("Cell is already occupied.")
            return False

    def demolish_building(self, x, y):
        if self.grid[y][x] != ".":
            self.grid[y][x] = "."
            # Deduct cost (1 coin), but do NOT block demolishing if coins low
            self.coins -= 1
            return True
        else:
            print("Cell is already empty.")
            return False

    def calculate_profit_and_upkeep(self):
        profit, upkeep = 0, 0
        road_segments = []
        clusters = []
        visited = set()

        # Find residential clusters for upkeep calculation
        def dfs(x, y, cluster):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                cluster.append((cx, cy))
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                        if self.grid[ny][nx] == "R" and (nx, ny) not in visited:
                            stack.append((nx, ny))

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cell = self.grid[y][x]
                if cell == "R" and (x, y) not in visited:
                    cluster = []
                    dfs(x, y, cluster)
                    clusters.append(cluster)
                elif cell == "I":
                    profit += 2
                    upkeep += 1
                elif cell == "C":
                    profit += 3
                    upkeep += 2
                elif cell == "O":
                    upkeep += 1
                elif cell == "*":
                    road_segments.append((x, y))

        # Each residential generates 1 coin profit
        profit += len([cell for row in self.grid for cell in row if cell == "R"])
        # Residential clusters upkeep cost
        upkeep += len(clusters)
        # Each road costs upkeep
        upkeep += len(road_segments)

        return profit, upkeep

    def calculate_score(self):
        # Implement scoring per original rules (simplified version):
        score = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cell = self.grid[y][x]

                if cell == "R":
                    # Check adjacency for industry
                    adjacent = self.get_adjacent_cells(x, y)
                    if "I" in adjacent:
                        score += 1
                    else:
                        # 1 point for each adjacent R or C
                        score += adjacent.count("R") + adjacent.count("C")
                        # 2 points for each adjacent park (O)
                        score += 2 * adjacent.count("O")

                elif cell == "I":
                    # 1 point per industry in city (counted later)
                    pass
                elif cell == "C":
                    # 1 point per adjacent commercial
                    adjacent = self.get_adjacent_cells(x, y)
                    score += adjacent.count("C")
                elif cell == "O":
                    # 1 point per adjacent park
                    adjacent = self.get_adjacent_cells(x, y)
                    score += adjacent.count("O")
                elif cell == "*":
                    # Score 1 point per connected road in same row
                    # Simplified: count total connected '*' in the same row
                    row = self.grid[y]
                    connected_roads = 0
                    for i in range(len(row)):
                        if row[i] == "*":
                            connected_roads += 1
                    score += connected_roads

        # Add 1 point per Industry (I) in the city (as per rules)
        total_industries = sum(row.count("I") for row in self.grid)
        score += total_industries

        return score

    def get_adjacent_cells(self, x, y):
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                adj.append(self.grid[ny][nx])
        return adj

    def next_turn(self):
        profit, upkeep = self.calculate_profit_and_upkeep()
        net = profit - upkeep
        self.coins += net  # Keep coins updated for reference, but no blocking

        if net < 0:
            self.loss_turns += 1
        else:
            self.loss_turns = 0

        self.score = self.calculate_score()
        self.turn += 1
        return net

    def display_status(self):
        print(f"\nTurn: {self.turn}")
        print("Coins: Unlimited")
        print(f"Score: {self.score}")
        profit, upkeep = self.calculate_profit_and_upkeep()
        print(f"Profit: {profit}, Upkeep: {upkeep}, Net: {profit - upkeep}")
        for row in self.grid:
            print(" ".join(row))

    def is_game_over(self):
        return self.loss_turns >= self.max_loss_turns



