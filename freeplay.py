import pygame
from mapv2 import Map  # Make sure mapv2.py is in the same folder

# Your FreePlayGame class code here (copy-paste your entire class)
# --------------------------------------------------------------
class FreePlayGame:
    def __init__(self):
        self.grid = self.create_grid(5)
        self.turn = 0
        self.loss_turns = 0
        self.max_loss_turns = 20
        self.coins = 1000  # Starting coins for display only, treated as unlimited
        self.score = 0     # Total score for the city

    def create_grid(self, size):
        return [["." for _ in range(size)] for _ in range(size)]

    def expand_grid_if_on_border(self, x, y, expansion_size=5):
        grid_size = len(self.grid)
        if x == 0 or y == 0 or x == grid_size - 1 or y == grid_size - 1:
            new_size = grid_size + 2 * expansion_size
            new_grid = self.create_grid(new_size)
            offset = expansion_size

            for old_y in range(grid_size):
                for old_x in range(grid_size):
                    new_grid[old_y + offset][old_x + offset] = self.grid[old_y][old_x]

            self.grid = new_grid
            return x + offset, y + offset
        return x, y

    def place_building(self, building, x, y):
        x, y = self.expand_grid_if_on_border(x, y)
        if self.grid[y][x] == ".":
            self.grid[y][x] = building
            self.coins -= 1  
            return True
        else:
            print("Cell is already occupied.")
            return False

    def demolish_building(self, x, y):
        if self.grid[y][x] != ".":
            self.grid[y][x] = "."
            self.coins -= 1
            return True
        else:
            print("Cell is already empty.")
            return False

    def calculate_profit_and_upkeep(self):
        profit, upkeep = 0, 0
        road_segments = []
        clusters = []
        visited = set()

        def dfs(x, y, cluster):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                cluster.append((cx, cy))
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                        if self.grid[ny][nx] == "R" and (nx, ny) not in visited:
                            stack.append((nx, ny))

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cell = self.grid[y][x]
                if cell == "R" and (x, y) not in visited:
                    cluster = []
                    dfs(x, y, cluster)
                    clusters.append(cluster)
                elif cell == "I":
                    profit += 2
                    upkeep += 1
                elif cell == "C":
                    profit += 3
                    upkeep += 2
                elif cell == "O":
                    upkeep += 1
                elif cell == "*":
                    road_segments.append((x, y))

        profit += len([cell for row in self.grid for cell in row if cell == "R"])
        upkeep += len(clusters)
        upkeep += len(road_segments)

        return profit, upkeep

    def calculate_score(self):
        score = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cell = self.grid[y][x]

                if cell == "R":
                    adjacent = self.get_adjacent_cells(x, y)
                    if "I" in adjacent:
                        score += 1
                    else:
                        score += adjacent.count("R") + adjacent.count("C")
                        score += 2 * adjacent.count("O")

                elif cell == "I":
                    pass
                elif cell == "C":
                    adjacent = self.get_adjacent_cells(x, y)
                    score += adjacent.count("C")
                elif cell == "O":
                    adjacent = self.get_adjacent_cells(x, y)
                    score += adjacent.count("O")
                elif cell == "*":
                    row = self.grid[y]
                    connected_roads = sum(1 for c in row if c == "*")
                    score += connected_roads

        total_industries = sum(row.count("I") for row in self.grid)
        score += total_industries

        return score

    def get_adjacent_cells(self, x, y):
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                adj.append(self.grid[ny][nx])
        return adj

    def next_turn(self):
        profit, upkeep = self.calculate_profit_and_upkeep()
        net = profit - upkeep
        self.coins += net

        if net < 0:
            self.loss_turns += 1
        else:
            self.loss_turns = 0

        self.score = self.calculate_score()
        self.turn += 1
        return net

    def display_status(self):
        print(f"\nTurn: {self.turn}")
        print("Coins: Unlimited")
        print(f"Score: {self.score}")
        profit, upkeep = self.calculate_profit_and_upkeep()
        print(f"Profit: {profit}, Upkeep: {upkeep}, Net: {profit - upkeep}")
        for row in self.grid:
            print(" ".join(row))

    def is_game_over(self):
        return self.loss_turns >= self.max_loss_turns

# --------------------------------------------------------------

SCREEN_WIDTH = 800
STATS_HEIGHT = 50

selected_building = "R"  # Default building

def draw_stats(screen, game, stats_height):
    font = pygame.font.SysFont("Arial", 20)
    screen.fill((220, 220, 220), (0, 0, screen.get_width(), stats_height))

    turn_text = font.render(f"Turn: {game.turn}", True, (0, 0, 0))
    coins_text = font.render(f"Coins: Unlimited", True, (0, 0, 0))
    score_text = font.render(f"Score: {game.score}", True, (0, 0, 0))
    profit, upkeep = game.calculate_profit_and_upkeep()
    net_text = font.render(f"Profit: {profit}  Upkeep: {upkeep}  Net: {profit - upkeep}", True, (0, 0, 0))

    screen.blit(turn_text, (10, 5))
    screen.blit(coins_text, (150, 5))
    screen.blit(score_text, (300, 5))
    screen.blit(net_text, (450, 5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("City Builder - Free Play Mode")
    city_map = Map(screen, GRID_SIZE)
    game = FreePlayGame(city_map)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        city_map.draw_grid()
        city_map.draw_buildings(game.grid)
        city_map.display_game_info(game.turn, game.coins, game.calculate_score())

        # Show two random building options
        selected_building, other_building = game.select_buildings()
        font = pygame.font.SysFont("Arial", 20)
        building_text = font.render(f"Choose a building: 1 - {selected_building}, 2 - {other_building}", True, BLACK)
        screen.blit(building_text, (20, 20))
        pygame.display.flip()

        placed = False
        building_choice = None

        while not placed and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        building_choice = selected_building
                    elif event.key == pygame.K_2:
                        building_choice = other_building
                elif event.type == pygame.MOUSEBUTTONDOWN and building_choice:
                    pos = pygame.mouse.get_pos()
                    row = (pos[1] - STATS_HEIGHT) // CELL_SIZE
                    col = pos[0] // CELL_SIZE

                    if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
                        continue  # Clicked outside the grid

                    if game.can_place(row, col):
                        game.place_building(building_choice, row, col)
                        city_map.grid[(row, col)] = building_choice

                        # Resize if needed
                        if len(game.grid) != city_map.grid_size:
                            game.grid_size = len(game.grid)
                            screen = pygame.display.set_mode((CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE + STATS_HEIGHT))
                            city_map = Map(screen, GRID_SIZE)
                            city_map.grid = game.grid

                        game.next_turn()

                        # ✅ GAME OVER CHECK
                        if game.is_game_over():
                            font = pygame.font.SysFont("Arial", 30)
                            game_over_text = font.render("Game Over: Loss for 20 turns", True, (255, 0, 0))
                            screen.blit(game_over_text, (200, STATS_HEIGHT + 20))
                            pygame.display.flip()
                            pygame.time.wait(4000)
                            running = False
                            break

                        placed = True

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()


