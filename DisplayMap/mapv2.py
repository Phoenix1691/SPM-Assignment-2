import pygame

# --- Colors ---
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BUILDING_COLORS = {
    "R": (255, 150, 150),
    "I": (200, 200, 100),
    "C": (150, 200, 255),
    "O": (180, 255, 180),
    "*": (150, 150, 150)
}

class Map:
    def __init__(self, grid_size, tile_size, stats_display_height):
        self.grid_size = grid_size  # e.g., 20 for 20x20
        self.tile_size = tile_size
        self.stats_display_height = stats_display_height
        self.grid = {}  # (row, col): building_type
        self.screen = None
        self.expansion_count = 0

    def initialize_screen(self):
        size = self.grid_size * self.tile_size
        self.screen = pygame.display.set_mode((size, size + self.stats_display_height))
        pygame.display.set_caption("City Map (Dict-based)")

    def draw(self):
        self.screen.fill(WHITE)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.tile_size
                y = row * self.tile_size + self.stats_display_height
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                # Determine cell color
                building = self.grid.get((row, col), "")
                color = BUILDING_COLORS.get(building, GRAY if (row + col) % 2 == 0 else WHITE)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def place_building(self, pos, building_type):
        """Places a building on a clicked cell"""
        x, y = pos
        if y < self.stats_display_height:
            return  # Ignore clicks on stats bar

        row = (y - self.stats_display_height) // self.tile_size
        col = x // self.tile_size

        # Check bounds
        if not (0 <= row < self.grid_size and 0 <= col < self.grid_size):
            return

        if (row, col) not in self.grid:
            self.grid[(row, col)] = building_type
            if self.is_on_border(row, col):
                self.expand_grid()

    def is_on_border(self, row, col):
        return row == 0 or col == 0 or row == self.grid_size - 1 or col == self.grid_size - 1

    def expand_grid(self):
        # Allow only 2 expansions: from 10 → 15, then 15 → 25
        if self.grid_size >= 25:
            print("Maximum grid size reached. Cannot expand further.")
            return

        expansion = 5
        new_grid = {}

            # Shift all existing buildings outward
        for (row, col), value in self.grid.items():
            new_row = row + expansion
            new_col = col + expansion
            new_grid[(new_row, new_col)] = value

        self.grid = new_grid
        self.grid_size += expansion * 2
        self.expansion_count += 1

        # Update window size
        size = self.grid_size * self.tile_size
        self.screen = pygame.display.set_mode((size, size + self.stats_display_height))

        print(f"Grid expanded to: {self.grid_size} x {self.grid_size}")


pygame.init()
pygame.font.init()

TILE_SIZE = 40
STATS_HEIGHT = 50
city_map = Map(10, TILE_SIZE, STATS_HEIGHT)
city_map.initialize_screen()

running = True
while running:
    city_map.draw()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            city_map.place_building(pygame.mouse.get_pos(), "R")

pygame.quit()