# mainMenu.py - Displays the main menu and handles user input

import pygame
import sys

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main Menu")

    # Main menu loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Clear the screen with black
        # Here you would draw your menu items

        pygame.display.flip()  # Update the display

main_menu()