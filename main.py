# File: main.py
# main.py - Main entry point for the game

import pygame
import sys
import mainMenu

pygame.init()

while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
