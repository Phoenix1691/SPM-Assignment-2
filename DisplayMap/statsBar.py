# statsBar.py
# statsBar.py - Displays and manages the stats bar in both Free Play and Arcade modes
# this will also have the game menu toggle functionality
import pygame

STATSBAR_BG = (200, 200, 200)
BLACK = (0, 0, 0)

BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER = (120, 120, 255)
TEXT_COLOR = (255, 255, 255)

def draw_stats_bar(surface, width, stats_display_height, font, stats_text):
    # Draw the stats display area
    stats_rect = pygame.Rect(0, 0, width, stats_display_height)
    pygame.draw.rect(surface, STATSBAR_BG, stats_rect)
    surface.blit(font.render(stats_text, True, BLACK), (10, 15))

# remove or rewrite code from here down
def draw_button(surface, rect, text, font, hovered):
    color = BUTTON_HOVER if hovered else BUTTON_COLOR
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)
    label = font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)

def draw_stats_bar_with_buttons(surface, width, height, font, message, mouse_pos):
    # Draw stats bar background
    stats_rect = pygame.Rect(0, 0, width, height)
    pygame.draw.rect(surface, STATSBAR_BG, stats_rect)

    # Draw text message
    label = font.render(message, True, BLACK)
    surface.blit(label, (10, 15))

    # Define buttons
    menu_button = pygame.Rect(width - 260, 10, 100, 40)
    build_button = pygame.Rect(width - 140, 10, 120, 40)

    draw_button(surface, menu_button, "Menu", font, menu_button.collidepoint(mouse_pos))

    return menu_button, build_button