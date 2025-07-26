# mainMenu.py - Displays the main menu and handles user input

import pygame
import sys
import pickle
from arcade_mode import main as arcade_main
from freeplay import FreePlayGame


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

def load_saved_game(filename="savegame.pkl"):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print("No saved game found.")
        return None

    mode = data.get('mode')
    if mode == 'arcade':
        from arcade_mode import ArcadeGame
        game = ArcadeGame()
    elif mode == 'freeplay':
        from freeplay import FreeplayGame
        game = FreeplayGame()
    else:
        print("Unknown saved game mode.")
        return None

    game.load_data(data)  # You must implement this in each class
    return game


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
            color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
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
                            arcade_main()
                        elif text == "Start New Free Play Game":
                            freeplay_main()
                        elif text == "Load Saved Game":
                            game = load_saved_game()
                            if game:
                                pygame.init()
                                info = pygame.display.Info()
                                screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
                                game.run()
                            else:
                                pygame.init()
                                main_menu()
                            return
                        elif text == "Display High Scores":
                            print("Display high scores clicked")
                        elif text == "Exit Game":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()

