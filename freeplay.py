import pygame
from mapv2 import Map  # Make sure mapv2.py is in the same folder

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 20
CELL_SIZE = 30
STATS_HEIGHT = 50

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
    def __init__(self, grid_size=GRID_SIZE):
        self.grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
        self.turn = 0
        self.loss_turns = 0
        self.max_loss_turns = 20
        self.score = 0
        self.selected_building = "R"
        self.demolish_mode = False

    def get_adjacent(self, x, y):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        adj = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(self.grid) and 0 <= nx < len(self.grid[0]):
                adj.append(self.grid[ny][nx])
        return adj

    def calculate_profit_and_upkeep(self):
        profit, upkeep = 0, 0
        road_connected = set()

        # Detect road segments connected horizontally
        for y, row in enumerate(self.grid):
            start = None
            for x, cell in enumerate(row + ["."]):  # Sentinel
                if cell == "*":
                    if start is None:
                        start = x
                else:
                    if start is not None:
                        if x - start > 1:
                            for rx in range(start, x):
                                road_connected.add((rx, y))
                        start = None

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                cell = self.grid[y][x]
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
                    if (x, y) not in road_connected:
                        upkeep += 1

        return profit, upkeep

    def calculate_score(self):
        score = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cell = self.grid[y][x]
                adj = self.get_adjacent(x, y)
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
                    score += sum(1 for c in self.grid[y] if c == "*")
        score += sum(row.count("I") for row in self.grid)
        return score

    def place_building(self, x, y):
        if self.grid[y][x] == ".":
            self.grid[y][x] = self.selected_building
            return True
        return False

    def demolish_building(self, x, y):
        if self.grid[y][x] != ".":
            self.grid[y][x] = "."
            return True
        return False

    def next_turn(self):
        profit, upkeep = self.calculate_profit_and_upkeep()
        net = profit - upkeep
        if net < 0:
            self.loss_turns += 1
        else:
            self.loss_turns = 0
        self.turn += 1
        self.score = self.calculate_score()

    def is_game_over(self):
        return self.loss_turns >= self.max_loss_turns

    def save(self, filename="savegame.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename="savegame.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                return pickle.load(f)
        return None

def draw_grid(screen, game):
    for y in range(len(game.grid)):
        for x in range(len(game.grid[y])):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + STATS_HEIGHT, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            font = pygame.font.SysFont("Arial", 20)
            cell = game.grid[y][x]
            if cell != ".":
                label = font.render(cell, True, BLACK)
                screen.blit(label, (rect.x + 8, rect.y + 5))

def draw_stats(screen, game):
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, STATS_HEIGHT))
    font = pygame.font.SysFont("Arial", 20)
    profit, upkeep = game.calculate_profit_and_upkeep()
    stats = f"Turn: {game.turn}  |  Score: {game.score}  |  Profit: {profit}  |  Upkeep: {upkeep}  |  Net: {profit-upkeep}  |  Mode: {'Demolish' if game.demolish_mode else game.selected_building}"
    label = font.render(stats, True, BLACK)
    screen.blit(label, (10, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("City Builder - Free Play")

    game = FreePlayGame()
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid(screen, game)
        draw_stats(screen, game)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_BUILDING:
                    game.selected_building = KEY_TO_BUILDING[event.key]
                    game.demolish_mode = False
                elif event.key == pygame.K_d:
                    game.demolish_mode = not game.demolish_mode
                elif event.key == pygame.K_s:
                    game.save()
                    print("Game saved.")
                elif event.key == pygame.K_l:
                    loaded = FreePlayGame.load()
                    if loaded:
                        game = loaded
                        print("Game loaded.")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if my < STATS_HEIGHT:
                    continue
                x = mx // CELL_SIZE
                y = (my - STATS_HEIGHT) // CELL_SIZE
                if 0 <= x < len(game.grid[0]) and 0 <= y < len(game.grid):
                    if game.demolish_mode:
                        if game.demolish_building(x, y):
                            game.next_turn()
                    else:
                        if game.place_building(x, y):
                            game.next_turn()

        if game.is_game_over():
            font = pygame.font.SysFont("Arial", 40)
            label = font.render("Game Over: 20 turns of loss", True, (200, 0, 0))
            screen.blit(label, (100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

