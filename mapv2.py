import pygame
#mapv2.py
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
    def __init__(game_mode, self, grid_size, screen_width, stats_display_height):
        self.game_mode = game_mode
        self.grid_size = grid_size
        self.stats_display_height = stats_display_height
        self.tile_size = screen_width // grid_size
        self.grid = {}
        self.screen = None
        self.expansion_count = 0
        self.first_turn = True

    def attempt_place_building(self, pos, building_type):
        """Handles building placement logic based on game mode."""
        x, y = pos
        if y < self.stats_display_height:
            return False  # clicked on stats bar

        row = (y - self.stats_display_height) // self.tile_size
        col = x // self.tile_size

        if not (0 <= row < self.grid_size and 0 <= col < self.grid_size):
            return False  # out of bounds

        if (row, col) in self.grid:
            return False  # already occupied

        if self.first_turn:
            self.grid[(row, col)] = building_type
            if self.game_mode == "freeplay" and self.is_on_border(row, col):
                self.expand_grid()
            self.first_turn = False
            return True

        # Mode-specific rules
        if self.game_mode == "arcade":
            if not self.has_adjacent_building(row, col):
                print("Arcade mode: Must place next to an existing building.")
                return False

        self.grid[(row, col)] = building_type

        if self.game_mode == "freeplay" and self.is_on_border(row, col):
            self.expand_grid()

        return True

    def has_adjacent_building(self, row, col):
        """Check if there is a building adjacent to (row, col)."""
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj = (row + dr, col + dc)
            if adj in self.grid:
                return True
        return False


    def initialize_screen(self):
        screen_width = self.grid_size * self.tile_size
        screen_height = screen_width + self.stats_display_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Ngee Ann City")

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
                
    def draw_building_options(self, building_options, selected_index):
        font = pygame.font.SysFont("Arial", 24)
        for i, building in enumerate(building_options):
            color = BUILDING_COLORS.get(building, GRAY)
            x = 50 + i * 120
            y = 10
            pygame.draw.rect(self.screen, color, (x, y, 60, 30))
            pygame.draw.rect(self.screen, BLACK, (x, y, 60, 30), 2)

            if i == selected_index:
                pygame.draw.rect(self.screen, BLACK, (x - 4, y - 4, 68, 38), 3)

            label = font.render(building, True, BLACK)
            self.screen.blit(label, (x + 20, y + 5))

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
        if self.grid_size >= 25:
            print("Maximum grid size reached. Cannot expand further.")
            return

        expansion = 5
        new_grid = {}

        for (row, col), value in self.grid.items():
            new_row = row + expansion
            new_col = col + expansion
            new_grid[(new_row, new_col)] = value

        self.grid = new_grid
        self.grid_size += expansion * 2
        self.expansion_count += 1

        # 🔁 Recalculate tile size to fit updated grid in original window width
        screen_width = self.screen.get_width()
        self.tile_size = screen_width // self.grid_size

        # Update screen height as well
        screen_height = self.grid_size * self.tile_size + self.stats_display_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        print(f"Grid expanded to: {self.grid_size} x {self.grid_size} (Tile: {self.tile_size}px)")

"""
# Constants
SCREEN_WIDTH = 800
STATS_HEIGHT = 50
INITIAL_GRID_SIZE = 10

# Selected building type (e.g., from building selection module)
selected_building = "R"

pygame.init()
pygame.font.init()

city_map = Map(INITIAL_GRID_SIZE, SCREEN_WIDTH, STATS_HEIGHT)
city_map.initialize_screen()

# Main Loop
running = True
while running:
    city_map.draw()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            city_map.attempt_place_building(pos, selected_building)

pygame.quit()
"""

"""
dont delete need this for reference
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 600 
STATS_HEIGHT = 50
INITIAL_GRID_SIZE = 10

city_map = Map(grid_size=INITIAL_GRID_SIZE, screen_width=SCREEN_WIDTH, stats_display_height=STATS_HEIGHT)
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
"""
pygame.quit()
