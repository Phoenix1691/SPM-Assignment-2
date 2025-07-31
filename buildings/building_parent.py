# buildings/building_parent.py - Base class for all building types in the game
class Building:
    def __init__(self):
        self.type = None
        self.size = (1, 1)
        self.route_no = None
    
    def get_adjacent_buildings(self, grid, row, col):
        adjacent = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            neighbor = grid.get((r, c))
            if neighbor is not None:
                adjacent.append(neighbor)
        return adjacent

    def calculate_profit_and_upkeep(self, grid, row, col, mode="freeplay", visited=None):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def score(self, adjacent_buildings):
        raise NotImplementedError("This method should be overridden by subclasses.")
