# map.py - Displays the map of the game using both statsBar and grid
import pygame
from grid import Grid
from statsBar import draw_stats_bar
# from statsBar import draw_stats_bar_with_buttons
# import statsBar

#to take out once its linked with the main menu
pygame.init()
pygame.font.init()

# --- Constants ---
TILE_SIZE = 60
STATS_DISPLAY_HEIGHT = 60  # Height of the stats display area
STATSBAR_BG = (200, 200, 200)


# Font setup
FONT = pygame.font.SysFont('Arial', 24)

def draw_map(grid_size, font):
    # Draw the grid
    # Window setup
    SCREEN_WIDTH = grid_size * TILE_SIZE
    SCREEN_HEIGHT = grid_size * TILE_SIZE + STATS_DISPLAY_HEIGHT
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Test")
    grid = Grid(grid_size, TILE_SIZE, STATS_DISPLAY_HEIGHT)
    # --- Main Loop ---
    running = True
    while running:
        SCREEN.fill((255, 255, 255))  # Clear the screen with white
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle left mouse button click
                grid.handle_click(pygame.mouse.get_pos())
        # Draw the stats bar
        stats_text = "Stats: Click to toggle tiles"
        # uncomment later
        draw_stats_bar(SCREEN, SCREEN.get_width(), STATS_DISPLAY_HEIGHT, font, stats_text)
        grid.draw(SCREEN)  # Draw the grid on the screen
        # Draw the grid
        # # FROM HERE TO
        # menu_button, build_button = statsBar.draw_stats_bar_with_buttons(
        # SCREEN, SCREEN.get_width(), STATS_DISPLAY_HEIGHT, FONT,
        # "Stats: Click tiles to toggle", pygame.mouse.get_pos())
        # grid.draw(SCREEN)
        # # Handle button clicks
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #     x, y = event.pos
        #     if menu_button.collidepoint((x, y)):
        #         print("Game Menu button clicked!")
        #         # Toggle menu view or pause state
        #     else:
        #         grid.handle_click((x, y))

        # # HERE, delete or rewrite
        # Update the display
        pygame.display.flip()

draw_map(10, FONT)  # Example grid size of 10x10
