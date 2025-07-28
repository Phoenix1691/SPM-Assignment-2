# File: main.py
# main.py - Main entry point for the game

import pygame
import sys
import mainMenu

pygame.init()
pygame.font.init()

while (True):
    mainMenu.main_menu()  # Call the main menu function from mainMenu.py
