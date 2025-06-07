# statsBar.py
# statsBar.py - Displays and manages the stats bar in both Free Play and Arcade modes
# this will also have the game menu toggle functionality
import pygame

STATSBAR_BG = (200, 200, 200)
BLACK = (0, 0, 0)

def draw_stats_bar(surface, width, stats_display_height, font, stats_text):
    # Draw the stats display area
    stats_rect = pygame.Rect(0, 0, width, stats_display_height)
    pygame.draw.rect(surface, STATSBAR_BG, stats_rect)
    surface.blit(font.render(stats_text, True, BLACK), (10, 15))