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
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
 
    def draw(self, surface):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.tile_size
                y = row * self.tile_size + self.stats_display_size
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                color = WHITE if (row + col) % 2 == 0 else GRAY
                if self.grid[row][col] == 1:
                    color = GREEN
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)

    def handle_click(self, pos):
        x, y = pos
        if y < self.stats_display_size:
            return
        row = (y - self.stats_display_size) // self.tile_size
        col = x // self.tile_size
        if self.grid[row][col] == 0:
            self.grid[row][col] = 1
        else:
            self.grid[row][col] = 0