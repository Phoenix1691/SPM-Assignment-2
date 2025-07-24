import pygame
import sys
from arcade_mode import ArcadeGame, main as arcade_main
from freeplay import FreePlayGame, main as freeplay_main
import pickle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (180, 180, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("City Builder - Main Menu")
font = pygame.font.SysFont("Arial", 30)

buttons = {
    "Start New Arcade Game": pygame.Rect(250, 100, 300, 50),
    "Start New Free Play Game": pygame.Rect(250, 170, 300, 50),
    "Load Saved Game": pygame.Rect(250, 240, 300, 50),
    "Display High Scores": pygame.Rect(250, 310, 300, 50),
    "Exit Game": pygame.Rect(250, 380, 300, 50),
}

def draw_text_center(text, rect, color=BLACK):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def load_saved_game():
    # Implement loading saved game, e.g. arcade or freeplay - 
    # For demo, let's load arcade save if exists
    try:
        with open("arcade_save.pkl", "rb") as f:
            data = pickle.load(f)
        # Here, you'd create an ArcadeGame instance and restore state from `data`.
        print("Loaded arcade save data.")
        arcade_main()  # Or implement a dedicated load state
    except Exception as e:
        print("Failed to load saved game:", e)

def display_high_scores():
    # Stub: display dummy scores or load from file
    running = True
    while running:
        screen.fill(WHITE)
        title = font.render("High Scores (Top 10)", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        # Example static list:
        scores = [("Alice", 120), ("Bob", 100), ("Carol", 80)]
        y = 120
        for name, score in scores:
            score_text = font.render(f"{name}: {score}", True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, y))
            y += 40

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.display.flip()

def main_menu():
    running = True
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        for text, rect in buttons.items():
            if rect.collidepoint(mouse_pos):
                color = BUTTON_HOVER_COLOR
            else:
                color = BUTTON_COLOR
            pygame.draw.rect(screen, color, rect)
            draw_text_center(text, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for text, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if text == "Start New Arcade Game":
                            arcade_main()
                        elif text == "Start New Free Play Game":
                            freeplay_main()
                        elif text == "Load Saved Game":
                            load_saved_game()
                        elif text == "Display High Scores":
                            display_high_scores()
                        elif text == "Exit Game":
                            running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
