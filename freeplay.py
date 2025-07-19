import pygame
import os
import pickle
from mapv2 import Map  # Your mapv2.py with Map class

SCREEN_WIDTH = 800
STATS_HEIGHT = 50
GRID_SIZE = 20

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

KEY_TO_BUILDING = {
    pygame.K_1: "R",
    pygame.K_2: "I",
    pygame.K_3: "C",
    pygame.K_4: "O",
    pygame.K_5: "*"
}

class FreePlayGame:
    def __init__(self):
        self.map = Map(GRID_SIZE, SCREEN_WIDTH, STATS_HEIGHT)
        self.map.initialize_screen()
        self.turn = 0
        self.loss_turns = 0
        self.max_loss_turns = 20
        self.score = 0
        self.selected_building = "R"
        self.demolish_mode = False

    def get_adjacent(self, row, col):
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dy, col + dx
            if 0 <= r < self.map.grid_size and 0 <= c < self.map.grid_size:
                adj.append(self.map.grid.get((r, c), "."))
        return adj

    def calculate_profit_and_upkeep(self):
        profit, upkeep = 0, 0
        road_connected = set()

        # Detect road segments connected horizontally
        for row in range(self.map.grid_size):
            start = None
            for col in range(self.map.grid_size + 1):  # +1 for sentinel
                cell = self.map.grid.get((row, col), ".") if col < self.map.grid_size else "."
                if cell == "*":
                    if start is None:
                        start = col
                else:
                    if start is not None:
                        if col - start > 1:
                            for rx in range(start, col):
                                road_connected.add((row, rx))
                        start = None

        for (row, col), cell in self.map.grid.items():
            if cell == "R":
                profit += 1
            elif cell == "I":
                profit += 2
                upkeep += 1
            elif cell == "C":
                profit += 3
                upkeep += 2
            elif cell == "O":
                upkeep += 1
            elif cell == "*":
                if (row, col) not in road_connected:
                    upkeep += 1

        return profit, upkeep

    def calculate_score(self):
        score = 0
        for (row, col), cell in self.map.grid.items():
            adj = self.get_adjacent(row, col)
            if cell == "R":
                if "I" in adj:
                    score += 1
                else:
                    score += adj.count("R") + adj.count("C") + 2 * adj.count("O")
            elif cell == "I":
                score += 0
            elif cell == "C":
                score += adj.count("C")
            elif cell == "O":
                score += adj.count("O")
            elif cell == "*":
                # Count roads on same row
                row_cells = [self.map.grid.get((row, c), ".") for c in range(self.map.grid_size)]
                score += sum(1 for b in row_cells if b == "*")
        score += sum(1 for b in self.map.grid.values() if b == "I")
        return score

    def place_building(self, pos):
        if self.demolish_mode:
            return False, "Cannot place building in demolish mode."
        success = self.map.attempt_place_building(pos, self.selected_building)
        if success:
            self.turn += 1
            coins_gained = 0  # you can implement coins logic here if needed
            self.score = self.calculate_score()
            self.map.first_turn = False
            return True, "Building placed."
        return False, "Cannot place building here."

    def demolish_building(self, pos):
        x, y = pos
        row = (y - STATS_HEIGHT) // self.map.tile_size
        col = x // self.map.tile_size
        if (row, col) in self.map.grid:
            del self.map.grid[(row, col)]
            self.score = self.calculate_score()
            self.turn += 1
            return True, "Building demolished."
        return False, "No building to demolish here."

    def next_turn(self):
        profit, upkeep = self.calculate_profit_and_upkeep()
        net = profit - upkeep
        if net < 0:
            self.loss_turns += 1
        else:
            self.loss_turns = 0
        self.score = self.calculate_score()

    def is_game_over(self):
        return self.loss_turns >= self.max_loss_turns

def draw_stats(screen, game):
    font = pygame.font.SysFont("Arial", 20)
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, STATS_HEIGHT))
    profit, upkeep = game.calculate_profit_and_upkeep()
    net = profit - upkeep
    mode = "Demolish" if game.demolish_mode else game.selected_building
    stats = f"Turn: {game.turn} | Score: {game.score} | Profit: {profit} | Upkeep: {upkeep} | Net: {net} | Mode: {mode}"
    label = font.render(stats, True, BLACK)
    screen.blit(label, (10, 10))

def main():
    pygame.init()
    game = FreePlayGame()
    clock = pygame.time.Clock()
    message = ""

    while True:
        game.map.draw()
        draw_stats(game.map.screen, game)
        if message:
            font = pygame.font.SysFont("Arial", 20)
            msg_surface = font.render(message, True, (255, 0, 0))
            game.map.screen.blit(msg_surface, (10, STATS_HEIGHT + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_BUILDING:
                    game.selected_building = KEY_TO_BUILDING[event.key]
                    game.demolish_mode = False
                    message = f"Selected building: {game.selected_building}"
                elif event.key == pygame.K_d:
                    game.demolish_mode = not game.demolish_mode
                    message = "Demolish mode ON" if game.demolish_mode else "Demolish mode OFF"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if pos[1] < STATS_HEIGHT:
                    continue
                if game.demolish_mode:
                    success, msg = game.demolish_building(pos)
                    if success:
                        game.next_turn()
                    message = msg
                else:
                    success, msg = game.place_building(pos)
                    if success:
                        game.next_turn()
                    message = msg

        if game.is_game_over():
            font = pygame.font.SysFont("Arial", 40)
            label = font.render("Game Over: 20 turns of loss", True, (200, 0, 0))
            game.map.screen.blit(label, (100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
