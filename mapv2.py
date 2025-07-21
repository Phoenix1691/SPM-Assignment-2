import pygame
import os
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
import tkinter

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()  # Close the Tkinter window
print(f"Screen resolution: {width}x{height}")

class Map:
    def __init__(self, game_mode, grid_size, screen_width, stats_display_height):
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
        pygame.display.init()
        display_info = pygame.display.Info()
        screen_w = display_info.current_w
        screen_h = display_info.current_h
        print("Screen initialized:", screen_w, screen_h)
        print("Screen initialized:", screen_width, screen_height)


    def draw(self):
        self.screen.fill((255, 255, 255))  # Clear the screen

        font = pygame.font.SysFont("Arial", self.tile_size // 2)

        # Draw the entire grid (empty and filled cells)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.tile_size
                y = row * self.tile_size + self.stats_display_height
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                # Check if there's a building at this position
                building = self.grid.get((row, col), None)
                
                if building:
                    # Assign color based on building type
                    if building == "R":
                        color = (144, 238, 144)  # light green
                    elif building == "I":
                        color = (169, 169, 169)  # dark gray
                    elif building == "C":
                        color = (135, 206, 250)  # light blue
                    elif building == "O":
                        color = (238, 232, 170)  # khaki
                    elif building == "*":
                        color = (255, 99, 71)    # tomato (red)
                    else:
                        color = (211, 211, 211)  # light gray for default/unknown

                    pygame.draw.rect(self.screen, color, rect)
                    
                    # Draw the symbol in the center
                    text_surface = font.render(building, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)
                else:
                    # Empty cell - draw with alternating pattern
                    if (row + col) % 2 == 0:
                        color = (240, 240, 240)  # light gray
                    else:
                        color = (250, 250, 250)  # very light gray
                    pygame.draw.rect(self.screen, color, rect)

                # Draw grid lines
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)


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

        # Recalculate tile size to fit updated grid in original window width
        screen_width = self.screen.get_width()
        self.tile_size = screen_width // self.grid_size

        # Update screen height as well
        screen_height = self.grid_size * self.tile_size + self.stats_display_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        print(f"Grid expanded to: {self.grid_size} x {self.grid_size} (Tile: {self.tile_size}px)")

#TESTING CODE

# Constants
SCREEN_WIDTH = 600
STATS_HEIGHT = 50
INITIAL_GRID_SIZE = 10

# Selected building type (e.g., from building selection module)
selected_building = "R"

pygame.init()
pygame.font.init()

city_map = Map("freeplay", INITIAL_GRID_SIZE, SCREEN_WIDTH, STATS_HEIGHT)
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
