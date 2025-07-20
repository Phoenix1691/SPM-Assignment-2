"""
Press 1 or 2 for the randomized building
Press D - Demolish
Press S - Save game
"""

import pygame
import random
import pickle
from mapv2 import Map  # Ensure mapv2.py with Map class is in the same folder

SCREEN_WIDTH = 800
STATS_HEIGHT = 80
GRID_SIZE = 20

BUILDINGS = ['R', 'I', 'C', 'O', '*']

class ArcadeGame:
    def __init__(self):
        self.map = Map(GRID_SIZE, SCREEN_WIDTH, STATS_HEIGHT)
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
        row = (y - STATS_HEIGHT) // self.map.tile_size
        col = x // self.map.tile_size
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

    def calculate_coins_from_new_building(self, pos, building):
        x, y = pos
        row = (y - STATS_HEIGHT) // self.map.tile_size
        col = x // self.map.tile_size
        coins = 0
        adjacent_buildings = self.get_adjacent(row, col)

        if building == 'R':
            # Residential gets coins for each adjacent Industry or Commercial
            coins = adjacent_buildings.count('I') + adjacent_buildings.count('C')

        elif building == 'I':
            # Industry generates coins equal to adjacent Residentials
            coins = adjacent_buildings.count('R')

        elif building == 'C':
            # Commercial generates coins equal to adjacent Residentials
            coins = adjacent_buildings.count('R')

        # Parks and Roads generate no coins
        return coins

    def calculate_score(self):
        score = 0
        total_industries = sum(1 for b in self.map.grid.values() if b == "I")
        for (row, col), building in self.map.grid.items():
            if building == "R":
                adjacent = self.get_adjacent(row, col)
                if "I" in adjacent:
                    score += 1
                else:
                    score += adjacent.count("R") + adjacent.count("C")
                    score += 2 * adjacent.count("O")
            elif building == "I":
                score += 1  # Each industry gives 1 point
            elif building == "C":
                adjacent = self.get_adjacent(row, col)
                score += adjacent.count("C")
            elif building == "O":
                adjacent = self.get_adjacent(row, col)
                score += adjacent.count("O")
            elif building == "*":
                row_cells = [self.map.grid.get((row, c), ".") for c in range(self.map.grid_size)]
                connected_roads = sum(1 for b in row_cells if b == "*")
                score += connected_roads
        score += total_industries
        return score
    def save_game(self, filename="arcade_save.pkl"):
        data = {
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
def draw_stats(screen, game):
    font = pygame.font.SysFont("Arial", 24)
    screen.fill((230, 230, 230), (0, 0, SCREEN_WIDTH, STATS_HEIGHT))
    screen.blit(font.render(f"Turn: {game.turn}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Coins: {game.coins}", True, (0, 0, 0)), (150, 10))
    screen.blit(font.render(f"Score: {game.score}", True, (0, 0, 0)), (300, 10))
    screen.blit(font.render(f"1: {game.building_choices[0]}   2: {game.building_choices[1]}", True, (0, 0, 0)), (500, 10))

def main():
    pygame.init()
    game = ArcadeGame()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    placing_building = None
    demolishing = False
    message = ""

    while True:
        game.map.draw()
        draw_stats(game.map.screen, game)

        if message:
            msg_surface = font.render(message, True, (255, 0, 0))
            game.map.screen.blit(msg_surface, (10, STATS_HEIGHT + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    placing_building = game.building_choices[0]
                    demolishing = False
                    message = f"Placing building: {placing_building}. Click on grid."
                elif event.key == pygame.K_2:
                    placing_building = game.building_choices[1]
                    demolishing = False
                    message = f"Placing building: {placing_building}. Click on grid."
                elif event.key == pygame.K_d:
                    demolishing = True
                    placing_building = None
                    message = "Demolish mode: Click on building to demolish."
                elif event.key == pygame.K_s:
                    game.save_game()
                    message = "Game saved."
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if demolishing:
                    success, msg = game.demolish_building(pos)
                    message = msg
                elif placing_building:
                    success, msg = game.place_building(pos, placing_building)
                    if success:
                        placing_building = None
                    message = msg

        # End game if conditions met
        if game.game_over:
            message = "Game Over! Final Score: " + str(game.score)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()


