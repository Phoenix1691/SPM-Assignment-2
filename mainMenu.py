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

import pygame
from highscore import get_top_scores

def display_highscores_screen(screen):
    pygame.init()
    font = pygame.font.SysFont("Arial", 28)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 50))

        title = font.render("Top 10 Highscores", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 20))

        y = 80
        for mode in ["Freeplay", "Arcade"]:
            mode_title = font.render(f"{mode} Mode", True, (255, 255, 0))
            screen.blit(mode_title, (50, y))
            y += 40

            highscores = get_top_scores(mode)
            if not highscores:
                no_data = font.render("No scores yet.", True, (200, 200, 200))
                screen.blit(no_data, (70, y))
                y += 40
            else:
                for i, entry in enumerate(highscores):
                    line = font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
                    screen.blit(line, (70, y))
                    y += 30
            y += 30

        # Back button
        back_rect = pygame.Rect(20, screen.get_height() - 60, 150, 40)
        pygame.draw.rect(screen, (100, 100, 255), back_rect)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_rect.x + 30, back_rect.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False

        clock.tick(60)

def draw_text_center(screen, text, rect, font, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def load_saved_game(screen,filename="savegame.pkl"):
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
        from freeplay import FreePlayGame
        game = FreePlayGame(screen)
    else:
        print("Unknown saved game mode.")
        return None

    game.load_data(data)  # You must implement this in each class
    return game


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    # screen_info = pygame.display.Info()
    # screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
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
                            arcade_main()  # assumes arcade_main() manages its own loop and returns here when done
                        elif text == "Start New Free Play Game":
                            # Create fullscreen screen for Freeplay
                            fullscreen_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            game = FreePlayGame(fullscreen_screen)
                            game.run()
                            # After game ends, recreate main menu screen if needed:
                            screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

                        elif text == "Load Saved Game":
                            game = load_saved_game(screen)
                            if game:
                                game.run()  # run loaded game loop
                            else:
                                print("No saved game to load.")
                        elif text == "Display High Scores":
                            print("Display high scores clicked")
                            display_highscores_screen(screen)
                        elif text == "Exit Game":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()


