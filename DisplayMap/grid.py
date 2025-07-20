# grid.py - Displays map

import pygame
import sys

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

class Grid:
    def __init__(self, grid_size, tile_size, stats_display_size):
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.stats_display_size = stats_display_size
        self.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
 
    # def draw(self, surface):
    #     for row in range(self.grid_size):
    #         for col in range(self.grid_size):
    #             x = col * self.tile_size
    #             y = row * self.tile_size + self.stats_display_size
    #             rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
    #             color = WHITE if (row + col) % 2 == 0 else GRAY
    #             if self.grid[row][col] == 1:
    #                 color = GREEN
    #             pygame.draw.rect(surface, color, rect)
    #             pygame.draw.rect(surface, BLACK, rect, 1)
    def draw(self, surface):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.tile_size
                y = row * self.tile_size + self.stats_display_size
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                cell = self.grid[row][col]
                if cell is None:
                    color = WHITE if (row + col) % 2 == 0 else GRAY
                else:
                    color = getattr(cell, 'color', (100, 100, 100))

                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)

                # Draw symbol/text if building exists
                if cell and hasattr(cell, "type_identifier"):
                    font = pygame.font.SysFont('Arial', 20)
                    text = font.render(cell.type_identifier, True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    surface.blit(text, text_rect)


    def handle_click(self, pos):
        x, y = pos
        if y < self.stats_display_size:
            return
        row = (y - self.stats_display_size) // self.tile_size
        col = x // self.tile_size
        # change to build or demolish functionality in arcade/free play mode later, and uncomment the return statement
        # return row, col
        # if self.grid[row][col] == 0:
        #     self.grid[row][col] = 1
        # else:
        #     self.grid[row][col] = 0
        from buildings.residential import residential  # or any other building

        if self.grid[row][col] is None:
            self.grid[row][col] = residential()
        else:
            self.grid[row][col] = None

        
    def build(type):
        # Placeholder for building functionality
        pass

    def demolish(type):
        # Placeholder for destroying functionality
        pass