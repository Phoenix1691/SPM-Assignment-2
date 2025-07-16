# ArcadePlay.py - Main entry point for the Arcade mode
import pygame
import sys
import pygame
from mapv2 import Map

# Constants
SCREEN_WIDTH = 800
STATS_HEIGHT = 50
INITIAL_GRID_SIZE = 10

# Selected building type (e.g., from building selection module)
selected_building = "R"

# Setup
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