import pygame
import tkinter

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
UI_HEIGHT = 90  # or STATS_HEIGHT + BUTTON_HEIGHT + margin

class Map:
    def __init__(self, game_mode, grid_size, screen=None):
        self.game_mode = game_mode
        self.grid_size = grid_size
        self.grid = {}
        self.screen = screen  
        self.expansion_count = 0
        self.first_turn = True
        self.tile_size = 0  # To be set during screen init
        self.fixed_grid_pixel_size = 800
        self.top_margin = 0
        self.left_margin = 0
        self.dirty_tiles = set()
        self.minimap_surface = None
        self.minimap_dirty = True
        self.stats_bar_height = 100
        # self.screen = screen



    def initialize_screen(self):
        pygame.display.init()

        # Get screen resolution using tkinter
        root = tkinter.Tk()
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        root.destroy()

        # Adjust tile size to fit screen minus stats bar
        max_tile_size = 64
        usable_h = screen_h - self.stats_bar_height
        self.tile_size = max(16, min(max_tile_size, screen_w // self.grid_size, usable_h // self.grid_size))
        self.fixed_grid_pixel_size = self.tile_size * self.grid_size

        # Only create screen if not already provided
        if self.screen is None:
            self.screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)

        pygame.display.set_caption("Ngee Ann City")

        self.update_margins()

        print(f"Fullscreen: {screen_w}x{screen_h}")
        print(f"Tile size: {self.tile_size}")


    def update_margins(self):
        screen_w, screen_h = self.screen.get_size()
        available_h = screen_h - UI_HEIGHT
        self.left_margin = (screen_w - self.grid_size * self.tile_size) // 2
        self.top_margin = self.stats_bar_height + (available_h - self.grid_size * self.tile_size) // 2



    def attempt_place_building(self, pos, building_type):
        x, y = pos
        self.update_margins()

        if y < self.top_margin:
            return False

        col = (x - self.left_margin) // self.tile_size
        row = (y - self.top_margin) // self.tile_size

        if not (0 <= col < self.grid_size and 0 <= row < self.grid_size):
            return False

        if (row, col) in self.grid:
            return False

        if self.first_turn:
            self.grid[(row, col)] = building_type
            self.dirty_tiles.add((row, col))
            self.minimap_dirty = True
            if self.game_mode == "freeplay" and self.is_on_border(row, col):
                self.expand_grid()
            self.first_turn = False
            return True

        if self.game_mode == "arcade":
            if not self.has_adjacent_building(row, col):
                print("Arcade mode: Must place next to an existing building.")
                return False

        self.grid[(row, col)] = building_type
        self.dirty_tiles.add((row, col))
        self.minimap_dirty = True

        if self.game_mode == "freeplay" and self.is_on_border(row, col):
            self.expand_grid()

        return True


    def has_adjacent_building(self, row, col):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (row + dr, col + dc) in self.grid:
                return True
        return False

    def draw_minimap(self):
        if not self.screen:
            return

        minimap_tile = 10
        margin = 10

        minimap_width = self.grid_size * minimap_tile
        minimap_height = self.grid_size * minimap_tile

        screen_w, screen_h = self.screen.get_size()
        minimap_x = screen_w - minimap_width - margin
        minimap_y = screen_h - minimap_height - margin

        # Only rebuild the minimap surface if dirty
        if self.minimap_dirty or self.minimap_surface is None:
            self.minimap_surface = pygame.Surface((minimap_width, minimap_height))
            self.minimap_surface.fill((230, 230, 230))
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    color = (220, 220, 220)
                    if (row, col) in self.grid:
                        building = self.grid[(row, col)]
                        color = BUILDING_COLORS.get(building, (128, 128, 128))
                    x = col * minimap_tile
                    y = row * minimap_tile
                    pygame.draw.rect(self.minimap_surface, color, pygame.Rect(x, y, minimap_tile, minimap_tile))
            pygame.draw.rect(self.minimap_surface, BLACK, self.minimap_surface.get_rect(), 2)
            self.minimap_dirty = False

        # Label
        font = pygame.font.SysFont("Arial", 14)
        label = font.render("Mini-map", True, (0, 0, 0))
        self.screen.blit(label, (minimap_x, minimap_y - 20))

        # Blit cached surface
        self.screen.blit(self.minimap_surface, (minimap_x, minimap_y))

    def draw_stats_bar(self):
        screen_w, _ = self.screen.get_size()
        bar_top = 0

        bar_rect = pygame.Rect(0, bar_top, screen_w, self.stats_bar_height)
        pygame.draw.rect(self.screen, GRAY, bar_rect)
        font = pygame.font.SysFont("Arial", 20)
        text = f"Grid: {self.grid_size}x{self.grid_size} | Tile: {self.tile_size}px | Buildings: {len(self.grid)}"
        label = font.render(text, True, BLACK)
        self.screen.blit(label, (10, bar_top + 10))



    def draw(self):
        # self.screen.fill(WHITE)
        self.update_margins()
        font = pygame.font.SysFont("Arial", self.tile_size // 2)

        if not self.dirty_tiles:
            self.dirty_tiles = {(r, c) for r in range(self.grid_size) for c in range(self.grid_size)}

        for (row, col) in self.dirty_tiles:
            x = self.left_margin + col * self.tile_size
            y = self.top_margin + row * self.tile_size
            rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
            building = self.grid.get((row, col))

            if building:
                color = BUILDING_COLORS.get(building, (211, 211, 211))
                pygame.draw.rect(self.screen, color, rect)
                text_surface = font.render(building, True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)
            else:
                color = (240, 240, 240) if (row + col) % 2 == 0 else (250, 250, 250)
                pygame.draw.rect(self.screen, color, rect)

            pygame.draw.rect(self.screen, BLACK, rect, 1)

        self.dirty_tiles.clear()
        self.draw_minimap()
        self.draw_stats_bar()


    def is_on_border(self, row, col):
        return row == 0 or col == 0 or row == self.grid_size - 1 or col == self.grid_size - 1

    def expand_grid(self):
        expansion = 5
        self.expansion_count += 1

        # Shift existing buildings
        new_grid = {}
        for (row, col), value in self.grid.items():
            new_grid[(row + expansion, col + expansion)] = value
        self.grid = new_grid

        self.grid_size += expansion * 2

        if self.expansion_count % 3 == 1 and self.expansion_count > 1:
            self.tile_size += 4
            self.fixed_grid_pixel_size = self.tile_size * self.grid_size
            print(f"[Cycle Reset] Increased tile size to {self.tile_size}")
        else:
            self.tile_size = max(16, self.fixed_grid_pixel_size // self.grid_size)
            print(f"[Shrink] Adjusted tile size to {self.tile_size}")

        screen_width, screen_height = self.screen.get_size()
        required_width = self.grid_size * self.tile_size + 100
        required_height = self.grid_size * self.tile_size + 100

        if screen_width < required_width or screen_height < required_height:
            self.screen = pygame.display.set_mode((required_width, required_height), pygame.RESIZABLE)

        self.update_margins()
        self.dirty_tiles = {(r, c) for r in range(self.grid_size) for c in range(self.grid_size)}
        self.minimap_dirty = True
        print(f"Expanded to {self.grid_size} x {self.grid_size} | Tile: {self.tile_size}px")

# # --- Main Execution ---
# pygame.init()
# pygame.font.init()

# INITIAL_GRID_SIZE = 5
# selected_building = "R"
# city_map = Map("freeplay", INITIAL_GRID_SIZE)
# city_map.initialize_screen()

# running = True
# while running:
#     city_map.draw()
#     pygame.display.flip()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         elif event.type == pygame.VIDEORESIZE:
#             screen_w, screen_h = event.w, event.h
#             city_map.screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
#             usable_h = screen_h - city_map.stats_bar_height
#             city_map.tile_size = max(16, min(64, screen_w // city_map.grid_size, usable_h // city_map.grid_size))
#             city_map.fixed_grid_pixel_size = city_map.tile_size * city_map.grid_size
#             city_map.update_margins()


#         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             pos = pygame.mouse.get_pos()
#             city_map.attempt_place_building(pos, selected_building)

pygame.quit()
