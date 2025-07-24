# mainMenu.py - Displays the main menu and handles user input

import pygame
import sys
from arcade_mode import main as arcade_main
from freeplay import main as freeplay_main

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 100, 200)
BUTTON_HOVER_COLOR = (100, 150, 255)

# Setup buttons with their positions and sizes
buttons = {
    "Start New Arcade Game": pygame.Rect(250, 100, 300, 50),
    "Start New Free Play Game": pygame.Rect(250, 170, 300, 50),
    "Load Saved Game": pygame.Rect(250, 240, 300, 50),
    "Display High Scores": pygame.Rect(250, 310, 300, 50),
    "Exit Game": pygame.Rect(250, 380, 300, 50),
}

def draw_text_center(screen, text, rect, font, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main Menu")
    font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons
        for text, rect in buttons.items():
            if rect.collidepoint(mouse_pos):
                color = BUTTON_HOVER_COLOR
            else:
                color = BUTTON_COLOR
            pygame.draw.rect(screen, color, rect)
            draw_text_center(screen, text, rect, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for text, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if text == "Start New Arcade Game":
                            arcade_main()   # Run arcade mode
                        elif text == "Start New Free Play Game":
                            freeplay_main() # Run freeplay mode
                        elif text == "Load Saved Game":
                            # Implement your load saved game function here
                            print("Load saved game clicked")
                        elif text == "Display High Scores":
                            # Implement your high scores display here
                            print("Display high scores clicked")
                        elif text == "Exit Game":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
