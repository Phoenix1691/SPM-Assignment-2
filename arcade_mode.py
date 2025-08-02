# arcade_mode.py - Arcade mode for the game with randomized building choices
"""
Press 1 or 2 for the randomized building
Press D - Demolish
Press S - Save game
"""

import importlib
from tkinter import font
import pygame
import random
import pickle
from mapv2 import Map  # Ensure mapv2.py with Map class is in the same folder
from highscore import save_highscore
from tutorial import show_legend_and_tutorial
from scoring import ScoringSystem
from economy import GameEconomy
from ui_utils import get_player_name
from ui_utils import draw_full_top_ui
from scoring import get_connected_neighbors

LEGEND_ITEMS = {
    "R": "Residential",
    "I": "Industry",
    "C": "Commercial",
    "O": "Park",
    "*": "Road"
}

GRID_SIZE = 20
# UI layout constants
BUILDINGS = ['R', 'I', 'C', 'O', '*']

def get_building_class(type_identifier):
    mapping = {
        "R": "residential",
        "I": "industry",
        "C": "commercial",
        "O": "park",
        "*": "road"
    }
    module_name = mapping.get(type_identifier)
    if module_name:
        module = importlib.import_module(f"buildings.{module_name}")
        return getattr(module, module_name)
    return None

class ArcadeGame:
    def __init__(self, screen):
        self.map = Map("arcade", GRID_SIZE)
        self.map.screen = screen           # store the given screen
        self.map.initialize_screen()
        self.turn = 0
        self.coins = 16
        self.score = 0
        self.building_choices = self.random_building_choices()
        self.selected_building = None
        self.game_over = False
        self.economy = GameEconomy(self.map)
        self.score_system = ScoringSystem(self.map)

    def random_building_choices(self):
        return random.sample(BUILDINGS, 2)

    def place_building(self, pos, building):
        if self.coins < 1:
            return False, "No coins left."
        building_class = get_building_class(building)
        building_instance = building_class()
        success = self.map.attempt_place_building(pos, building_instance)

        if success:
            self.coins -= 1
            self.turn += 1
            self.coins += self.economy.generate_arcade_coins()

            # Update total score after placement
            self.score = self.calculate_total_score()
            print(f"[DEBUG] Total Score: {self.score}")

            self.building_choices = self.random_building_choices()
            self.map.first_turn = False

            # Check for game over: no coins or board full
            if self.coins <= 0 or len(self.map.grid) >= self.map.grid_size ** 2:
                self.game_over = True

            return True, f"Building placed. Coins: {self.coins}"
        else:
            return False, "Cannot place building here."

    def demolish_building(self, pos, building):
        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size

        if (row, col) in self.map.grid:
            if self.coins < 1:
                return False, "Not enough coins to demolish."
            del self.map.grid[(row, col)]
            self.coins -= 1
            # Update total score after demolition
            self.score = self.calculate_total_score()
            print(f"[DEBUG] Total Score: {self.score}")

            if len(self.map.grid) == 0:
                self.map.first_turn = True
            return True, "Building demolished."

        return False, "No building to demolish here."

    def get_adjacent(self, row, col):
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dy, col + dx
            if 0 <= r < self.map.grid_size and 0 <= c < self.map.grid_size:
                adj.append(self.map.grid.get((r, c), "."))
        return adj

    def calculate_total_score(self):
        total_score = 0
        for (row, col), building in self.map.grid.items():
            # Get building type identifier
            b_type = getattr(building, "type_identifier", building)
            building_class = get_building_class(b_type)
            if not building_class:
                continue
            building_instance = building_class()
            connected_counts = get_connected_neighbors(self.map.grid, (row, col))
            total_score += building_instance.score(connected_counts)
        return total_score
    def get_adjacent_counts(self, row, col):
        counts = {}
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dy, col + dx
            b = self.map.grid.get((r, c))
            if b:
                counts[b] = counts.get(b, 0) + 1
        return counts

    def save_game(self, filename="savegame.pkl"):
        data = {
            'mode': 'arcade',
            'grid': self.map.grid,
            'turn': self.turn,
            'coins': self.coins,
            'score': self.score,
            'building_choices': self.building_choices,
            'selected_building': self.selected_building,
            'game_over': self.game_over
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
    
    def load_data(self, data):
        self.map.grid = data['grid']
        self.turn = data['turn']
        self.coins = data['coins']
        self.score = data['score']
        self.building_choices = data['building_choices']
        self.selected_building = data['selected_building']
        self.game_over = data['game_over']
        
    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 20)

        placing_building = None
        demolishing = False
        message = ""
        show_tutorial = False

        while True:
            screen = self.map.screen
            screen.fill((230, 230, 230))
            self.map.draw()

            buttons = draw_full_top_ui(screen, self, message, building_choices=self.building_choices, demolish_mode=demolishing)
            # --- Events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if buttons["Menu"].collidepoint(pos):
                        from mainMenu import main_menu
                        main_menu()
                        return
                    elif buttons[self.building_choices[0]].collidepoint(pos):
                        placing_building = self.building_choices[0]
                        demolishing = False
                        message = f"Placing: {placing_building}"
                    elif buttons[self.building_choices[1]].collidepoint(pos):
                        placing_building = self.building_choices[1]
                        demolishing = False
                        message = f"Placing: {placing_building}"
                    elif buttons["Demolish"].collidepoint(pos):
                        demolishing = True
                        placing_building = None
                        message = "Demolish mode."
                    elif buttons["Save"].collidepoint(pos):
                        self.save_game()
                        message = "Game saved."
                    else:
                        msg = ""
                        if demolishing:
                            success, msg = self.demolish_building(pos, placing_building)
                        elif placing_building:
                            success, msg = self.place_building(pos, placing_building)
                            if success:
                                placing_building = None
                        message = msg

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        show_tutorial = not show_tutorial
                        if show_tutorial:
                            show_legend_and_tutorial(screen, "arcade")

            # --- Game Over ---
            if self.game_over:
                font_big = pygame.font.SysFont("Arial", 40)
                text_surface = font_big.render(f"Game Over! Final Score: {self.score}", True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                pygame.time.wait(3000)

                name = get_player_name(screen)
                if name:
                    save_highscore(name, self.score, "Arcade")

                from mainMenu import main_menu
                main_menu()
                return

            pygame.display.flip()
            clock.tick(30)

def main():
    pygame.init()
    # screen = pygame.display.set_mode((1280, 1000), pygame.NOFRAME)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    game = ArcadeGame(screen)
    game.run()

if __name__ == "__main__":
    main()

