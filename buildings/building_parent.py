class Building:
    def __init__(self):
        self.type = None
        self.size = (1, 1)

    def calculate_profit_and_upkeep(self, grid):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def score(self, adjacent_buildings):
        raise NotImplementedError("This method should be overridden by subclasses.")