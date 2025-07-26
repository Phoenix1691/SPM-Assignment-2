# freeplay.py - Free play mode for the city-building game
"""
Press 1: Residential (R)
Press 2: Industry (I)
Press 3: Commercial (C)
Press 4: Park (O)
Press 5: Road (*)
Press D: Demolish
Press S: Save game
"""

import pygame
import os
import pickle
from mapv2 import Map  # Your mapv2.py with Map class


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
STATS_HEIGHT = 50

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BUILDING_COLORS = {
    "R": (255, 150, 150),
    "I": (200, 200, 100),
    "C": (150, 200, 255),
    "O": (180, 255, 180),
    "*": (150, 150, 150),
    "D": (255, 0, 0),  # Demolish button color
    "Save": (100, 255, 100),
    "Menu": (255, 200, 0)
}

# Constants for buttons
BUILDING_OPTIONS = ["R", "I", "C", "O", "*", "D", "Save", "Menu"]
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
BUTTON_Y = 5
UI_HEIGHT = STATS_HEIGHT + BUTTON_HEIGHT + 20  # Add padding

class FreePlayGame:
    def __init__(self, screen):
        # self.map = Map(grid_size=5, screen_width=SCREEN_WIDTH, stats_display_height=STATS_HEIGHT)
        # self.map = Map("freeplay", grid_size=5, screen_width=SCREEN_WIDTH, stats_display_height=STATS_HEIGHT)
        self.map = Map("freeplay", grid_size=5, screen=screen)
        self.map.initialize_screen()
        self.turn = 0
        self.loss_turns = 0
        self.max_loss_turns = 20
        self.score = 0
        self.selected_building = "R"
        self.demolish_mode = False
        self.message = ""
        self.message_timer = 0


    def get_bounds(self):
        if not self.map.grid:
            return 0, self.map.grid_size - 1, 0, self.map.grid_size - 1
        rows = [pos[0] for pos in self.map.grid.keys()]
        cols = [pos[1] for pos in self.map.grid.keys()]
        return min(rows), max(rows), min(cols), max(cols)

    def get_adjacent(self, row, col):
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dy, col + dx
            adj.append(self.map.grid.get((r, c), "."))
        return adj

    def calculate_profit_and_upkeep(self):
        profit, upkeep = 0, 0

        # Check profit and upkeep for each building type
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
                # Road upkeep: cost if no adjacent road segment
                connected = False
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    adj_cell = self.map.grid.get((row + dy, col + dx))
                    if adj_cell == "*":
                        connected = True
                        break
                if not connected:
                    upkeep += 1

        # Residential cluster upkeep: 1 coin per cluster of connected R's
        visited = set()
        def dfs(r, c):
            stack = [(r, c)]
            while stack:
                rr, cc = stack.pop()
                if (rr, cc) in visited:
                    continue
                visited.add((rr, cc))
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = rr + dy, cc + dx
                    if self.map.grid.get((nr, nc)) == "R" and (nr, nc) not in visited:
                        stack.append((nr, nc))

        for (row, col), cell in self.map.grid.items():
            if cell == "R" and (row, col) not in visited:
                dfs(row, col)
                upkeep += 1

        return profit, upkeep

    def calculate_score(self):
        score = 0
        min_row, max_row, min_col, max_col = self.get_bounds()

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                cell = self.map.grid.get((row, col), ".")
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
                    score += 1
        score += sum(1 for b in self.map.grid.values() if b == "I")
        return score

    def place_building(self, pos):
        if self.demolish_mode:
            return False, "Cannot place building in demolish mode."

        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size
        if row < 0 or col < 0 or row >= self.map.grid_size or col >= self.map.grid_size:
            return False, "Invalid placement."
        if (row, col) not in self.map.grid:
            self.map.grid[(row, col)] = self.selected_building

            if self.map.is_on_border(row, col):
                self.map.expand_grid()

            self.turn += 1
            self.score = self.calculate_score()
            self.map.first_turn = False
            return True, "Building placed."
        else:
            return False, "Cell already occupied."


    
    def demolish_building(self, pos):
        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size
        if row < 0 or col < 0 or row >= self.map.grid_size or col >= self.map.grid_size:
            return False, "Invalid placement."
        if (row, col) in self.map.grid:
            del self.map.grid[(row, col)]
            self.turn += 1
            self.score = self.calculate_score()
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

    def save_game(self, filename="savegame.pkl"):
        data = {
            'mode': 'freeplay',
            'grid': self.map.grid,
            'turn': self.turn,
            'loss_turns': self.loss_turns,
            'score': self.score
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        self.show_message("Game saved successfully!")
        return True

    
    def load_data(self, data):
        self.map.grid = data['grid']
        self.turn = data['turn']
        self.loss_turns = data['loss_turns']
        self.score = data['score']

    def show_message(self, msg, duration=120):
        self.message = msg
        self.message_timer = duration

def draw_stats(screen, game):
    font = pygame.font.SysFont("Arial", 20)
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, STATS_HEIGHT))
    
    profit, upkeep = game.calculate_profit_and_upkeep()
    net = profit - upkeep
    mode = "Demolish" if game.demolish_mode else game.selected_building
    stats = f"Turn: {game.turn} | Score: {game.score} | Profit: {profit} | Upkeep: {upkeep} | Net: {net} | Mode: {mode}"
    
    label = font.render(stats, True, BLACK)
    screen.fill(WHITE, (0, 0, SCREEN_WIDTH, STATS_HEIGHT))
    screen.blit(label, (10, BUTTON_HEIGHT + 10))  # Adjusted Y-position to avoid overlapping buttons

# def draw_building_buttons(screen, selected_building, demolish_mode):
#     font = pygame.font.SysFont("Arial", 20)
#     buttons = {}
#     x_offset = BUTTON_MARGIN
#     for option in BUILDING_OPTIONS:
#         color = GRAY
#         if demolish_mode:
#             if option == "D":
#                 color = (255, 100, 100)  # Highlight demolish mode in red
#         else:
#             if option == selected_building:
#                 color = (100, 255, 100)  # Highlight selected building in green


#         rect = pygame.Rect(x_offset, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
#         pygame.draw.rect(screen, color, rect)
#         pygame.draw.rect(screen, BLACK, rect, 2)  # border

#         label_text = "Demolish" if option == "D" else option
#         label = font.render(label_text, True, BLACK)
#         label_rect = label.get_rect(center=rect.center)
#         screen.blit(label, label_rect)

#         buttons[option] = rect
#         x_offset += BUTTON_WIDTH + BUTTON_MARGIN

#     return buttons

def draw_building_buttons(screen, selected_building, demolish_mode):
    font = pygame.font.SysFont("Arial", 20)
    buttons = {}
    x_offset = BUTTON_MARGIN

    for option in BUILDING_OPTIONS:
        color = GRAY
        if option == selected_building and not demolish_mode:
            color = BUILDING_COLORS.get(option, GRAY)
        elif option == "D" and demolish_mode:
            color = BUILDING_COLORS["D"]
        elif option in ["Save", "Menu"]:
            color = BUILDING_COLORS.get(option, GRAY)

        rect = pygame.Rect(x_offset, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        label_text = option if option not in ["D"] else "Demolish"
        label = font.render(label_text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

        buttons[option] = rect
        x_offset += BUTTON_WIDTH + BUTTON_MARGIN

    return buttons


def handle_button_click(pos, buttons, game):
    for option, rect in buttons.items():
        if rect.collidepoint(pos):
            if option == "D":
                game.demolish_mode = not game.demolish_mode
                game.show_message("Demolish mode " + ("ON" if game.demolish_mode else "OFF"))
            elif option == "Save":
                game.save_game()
            elif option == "Menu":
                from mainMenu import main_menu
                pygame.quit()
                main_menu()
            else:
                game.selected_building = option
                game.demolish_mode = False
                game.show_message(f"Selected: {option}")
            return True
    return False

def main():
    pygame.init()
    pygame.display.set_caption("Freeplay Game")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = FreePlayGame(screen)

    while True:
        screen.fill(WHITE)
        game.map.draw()
        draw_stats(screen, game)
        buttons = draw_building_buttons(screen, game.selected_building, game.demolish_mode)

        if game.message_timer > 0:
            font = pygame.font.SysFont("Arial", 20)
            msg_surface = font.render(game.message, True, RED)
            screen.blit(msg_surface, (10, STATS_HEIGHT + BUTTON_HEIGHT + 15))
            game.message_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if pos[1] < UI_HEIGHT:
                    if handle_button_click(pos, buttons, game):
                        continue
                if game.demolish_mode:
                    success, msg = game.demolish_building(pos)
                    if success:
                        game.turn += 1
                    game.show_message(msg)
                else:
                    success, msg = game.place_building(pos)
                    if success:
                        game.turn += 1
                    game.show_message(msg)

        if game.is_game_over():
            font = pygame.font.SysFont("Arial", 40)
            label = font.render("Game Over: 20 turns of loss", True, RED)
            screen.blit(label, (100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            return

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()


