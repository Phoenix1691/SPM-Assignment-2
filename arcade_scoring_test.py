# arcade_scoring_test.py

from pprint import pprint

# Constants for tiles
EMPTY = '*'
RESIDENTIAL = 'R'
INDUSTRIAL = 'I'
COMMERCIAL = 'C'

class ArcadeGrid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
    
    def place_tile(self, r, c, tile):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = tile
        else:
            print(f"Invalid placement position: ({r}, {c})")
    
    def print_grid(self):
        for row in self.grid:
            print(" ".join(row))
    
    def get_adjacent_tiles(self, r, c):
        adjacents = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                adjacents.append((nr, nc, self.grid[nr][nc]))
        return adjacents
    
    def score_tile(self, r, c):
        tile = self.grid[r][c]
        if tile not in (INDUSTRIAL, COMMERCIAL):
            return 0
        
        adjacents = self.get_adjacent_tiles(r, c)
        score = 0
        debug_info = []
        for nr, nc, adj_tile in adjacents:
            debug_info.append(f"  Checking tile at ({nr}, {nc}): {adj_tile}")
            if adj_tile == RESIDENTIAL:
                score += 1
        
        print(f"Scoring for {tile} at ({r}, {c})")
        for line in debug_info:
            print(line)
        print(f"Score returned: {score}")
        return score
    
    def score_all(self):
        total_score = 0
        print("\nStarting scoring turn...")
        print("Grid:")
        self.print_grid()
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.grid[r][c]
                if tile in (INDUSTRIAL, COMMERCIAL):
                    total_score += self.score_tile(r, c)
        print(f"Score gained this turn: {total_score}\n{'-'*40}")
        return total_score

def run_simulation():
    # Setup a 5x5 grid for testing
    grid = ArcadeGrid(5, 5)
    
    # Sequence of placements simulating turns:
    # (row, col, tile)
    turns = [
        (2, 2, RESIDENTIAL),    # Turn 1: Place R center
        (2, 1, INDUSTRIAL),     # Turn 2: Place I left of R
        (2, 3, COMMERCIAL),     # Turn 3: Place C right of R
        (1, 2, RESIDENTIAL),    # Turn 4: Place R above center
        (3, 2, RESIDENTIAL),    # Turn 5: Place R below center
        (1, 1, INDUSTRIAL),     # Turn 6: Place I top-left corner near R
        (3, 3, COMMERCIAL),     # Turn 7: Place C bottom-right near R
        (0, 2, RESIDENTIAL),    # Turn 8: Place R two rows above center
        (4, 2, RESIDENTIAL),    # Turn 9: Place R two rows below center
        (0, 1, INDUSTRIAL),     # Turn 10: Place I near R at (0,2)
        (4, 3, COMMERCIAL),     # Turn 11: Place C near R at (4,2)
    ]
    
    total_score = 0
    
    for i, (r, c, tile) in enumerate(turns, start=1):
        print(f"Turn {i}: Placing {tile} at ({r}, {c})")
        grid.place_tile(r, c, tile)
        # After each placement, score all relevant tiles
        turn_score = grid.score_all()
        total_score += turn_score
    
    print(f"Total score after all turns: {total_score}")

if __name__ == "__main__":
    run_simulation()
