import pygame
import sys
from ArcadeMode import ArcadePlay
from FreePlayMode import FreePlay

pygame.init()

while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
