# arcade_mode.py - Arcade mode for the game with randomized building choices
"""
Press 1 or 2 for the randomized building
Press D - Demolish
Press S - Save game
"""

import importlib
import pygame
import random
import pickle
from mapv2 import Map  # Ensure mapv2.py with Map class is in the same folder

SCREEN_WIDTH = 800
STATS_HEIGHT = 80
GRID_SIZE = 20

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
    def __init__(self):
        # self.map = Map(GRID_SIZE, SCREEN_WIDTH, STATS_HEIGHT)
        # self.map = Map("arcade", GRID_SIZE, SCREEN_WIDTH, STATS_HEIGHT)
        self.map = Map("arcade", GRID_SIZE)
        self.map.initialize_screen()
        self.turn = 0
        self.coins = 16
        self.score = 0
        self.building_choices = self.random_building_choices()
        self.selected_building = None
        self.game_over = False

    def random_building_choices(self):
        return random.sample(BUILDINGS, 2)

    def place_building(self, pos, building):
        if self.coins < 1:
            return False, "No coins left."
        success = self.map.attempt_place_building(pos, building)
        if success:

            self.coins -= 1
            self.turn += 1

            # Calculate coins earned based on new building adjacency
            coins_gained = self.calculate_coins_from_new_building(pos, building)
            self.coins += coins_gained

            self.score = self.calculate_score()
            self.building_choices = self.random_building_choices()
            self.map.first_turn = False

            # Check for game over: no coins or board full
            if self.coins <= 0 or len(self.map.grid) >= self.map.grid_size ** 2:
                self.game_over = True

            return True, f"Building placed. Coins gained: {coins_gained}"
        else:
            return False, "Cannot place building here."

    def demolish_building(self, pos):
        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size

        if (row, col) in self.map.grid:
            if self.coins < 1:
                return False, "Not enough coins to demolish."
            del self.map.grid[(row, col)]
            self.coins -= 1
            self.score = self.calculate_score()
            return True, "Building demolished."
        return False, "No building to demolish here."

    def get_adjacent(self, row, col):
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dy, col + dx
            if 0 <= r < self.map.grid_size and 0 <= c < self.map.grid_size:
                adj.append(self.map.grid.get((r, c), "."))
        return adj

    def calculate_coins_from_new_building(self, pos, building_type):
        x, y = pos
        row = (y - STATS_HEIGHT) // self.map.tile_size
        col = x // self.map.tile_size

        building_class = get_building_class(building_type)
        if not building_class:
            return 0
        building = building_class()
        profit, upkeep = building.calculate_profit_and_upkeep(self.map.grid)
        return profit - upkeep

    def calculate_score(self):
        score = 0
        for (row, col), building_type in self.map.grid.items():
            building_class = get_building_class(building_type)
            if not building_class:
                continue
            building = building_class()
            adj = self.get_adjacent_counts(row, col)
            score += building.score(adj)
        return score
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

        button1 = pygame.Rect(500, 10, 40, 30)
        button2 = pygame.Rect(550, 10, 40, 30)
        demolish_btn = pygame.Rect(610, 10, 90, 30)
        save_btn = pygame.Rect(710, 10, 80, 30)
        main_menu_btn = pygame.Rect(610, 50, 180, 30)

        while True:
            self.map.draw()
            draw_stats(self.map.screen, self)

            pygame.draw.rect(self.map.screen, (180, 180, 255), button1)
            pygame.draw.rect(self.map.screen, (180, 180, 255), button2)
            pygame.draw.rect(self.map.screen, (255, 180, 180), demolish_btn)
            pygame.draw.rect(self.map.screen, (180, 255, 180), save_btn)

            pygame.draw.rect(self.map.screen, (200, 200, 200), main_menu_btn)
            pygame.draw.rect(self.map.screen, (0, 0, 0), main_menu_btn, 2)
            self.map.screen.blit(font.render("Main Menu", True, (0, 0, 0)), main_menu_btn.move(40, 5))

            self.map.screen.blit(font.render(self.building_choices[0], True, (0, 0, 0)), button1.move(10, 5))
            self.map.screen.blit(font.render(self.building_choices[1], True, (0, 0, 0)), button2.move(10, 5))
            self.map.screen.blit(font.render("Demolish", True, (0, 0, 0)), demolish_btn.move(5, 5))
            self.map.screen.blit(font.render("Save", True, (0, 0, 0)), save_btn.move(10, 5))

            if message:
                msg_surface = font.render(message, True, (255, 0, 0))
                self.map.screen.blit(msg_surface, (10, STATS_HEIGHT + 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if main_menu_btn.collidepoint(pos):
                        pygame.quit()
                        from mainMenu import main_menu
                        main_menu()
                        return

                    if button1.collidepoint(pos):
                        placing_building = self.building_choices[0]
                        demolishing = False
                        message = f"Placing: {placing_building}"
                    elif button2.collidepoint(pos):
                        placing_building = self.building_choices[1]
                        demolishing = False
                        message = f"Placing: {placing_building}"
                    elif demolish_btn.collidepoint(pos):
                        demolishing = True
                        placing_building = None
                        message = "Demolish mode."
                    elif save_btn.collidepoint(pos):
                        self.save_game()
                        message = "Game saved."
                    else:
                        msg = ""
                        if demolishing:
                            success, msg = self.demolish_building(pos)
                        elif placing_building:
                            success, msg = self.place_building(pos, placing_building)
                            if success:
                                placing_building = None
                        message = msg

            if self.game_over:
                message = "Game Over! Final Score: " + str(self.score)

            pygame.display.flip()
            clock.tick(30)



def draw_stats(screen, game):
    font = pygame.font.SysFont("Arial", 24)
    screen.fill((230, 230, 230), (0, 0, SCREEN_WIDTH, STATS_HEIGHT))
    screen.blit(font.render(f"Turn: {game.turn}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Coins: {game.coins}", True, (0, 0, 0)), (150, 10))
    screen.blit(font.render(f"Score: {game.score}", True, (0, 0, 0)), (300, 10))

def main():
    game = ArcadeGame()
    game.run()
    

if __name__ == "__main__":
    main()
