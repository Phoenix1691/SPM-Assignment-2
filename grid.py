import pygame
import sys

pygame.init()

# --- Constants ---
GRID_SIZE = 8
TILE_SIZE = 60
STATS_DISPLAY_SIZE = 60  # Size of the stats display area

# --- Colours (Colors) ---
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
HUD_BG = (200, 200, 200)
def draw_grid(surface, grid):
    """Draw the grid on the given surface."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE + STATS_DISPLAY_SIZE, TILE_SIZE, TILE_SIZE)
            color = WHITE if (row + col) % 2 == 0 else GRAY
            if grid[row][col] == 1:
                color = GREEN
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
# Window setup
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE + STATS_DISPLAY_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Test")

# Font setup
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)

# Initialize the grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < STATS_DISPLAY_SIZE:
                continue  # Ignore clicks in the stats display area
            # Calculate the grid cell based on mouse position
            col = x // TILE_SIZE
            row = (y - STATS_DISPLAY_SIZE) // TILE_SIZE
            if grid[row][col] == 0:
                grid[row][col] = 1
            elif grid[row][col] == 1:
                grid[row][col] = 0

    # Clear the screen
    SCREEN.fill(HUD_BG)

    # Draw the stats display area
    stats_rect = pygame.Rect(0, 0, SCREEN_WIDTH, STATS_DISPLAY_SIZE)
    pygame.draw.rect(SCREEN, WHITE, stats_rect)
    SCREEN.blit(FONT.render("Click to toggle tiles", True, BLACK), (10, 15))

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE + STATS_DISPLAY_SIZE, TILE_SIZE, TILE_SIZE)
            color = WHITE if (row + col) % 2 == 0 else GRAY
            if grid[row][col] == 1:
                color = GREEN
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

    pygame.display.flip()

pygame.quit()
sys.exit()
