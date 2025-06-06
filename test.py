import pygame
import sys

pygame.init()

GRAY = (180, 180, 180)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
HUD_BG = (200, 200, 200)


grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // TILE_SIZE
            row = y // TILE_SIZE
            if grid[row][col] == 0:
                grid[row][col] = 1
            elif grid[row][col] == 1:
                grid[row][col] = 0

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = WHITE if (row + col) % 2 == 0 else GRAY
            if grid[row][col] == 1:
                color = GREEN
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

    pygame.display.flip()

pygame.quit()
sys.exit()
