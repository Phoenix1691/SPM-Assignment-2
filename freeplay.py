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
from ui_utils import draw_button
from tutorial import show_legend_and_tutorial
from buildings.residential import residential
from buildings.industry import industry
from buildings.commercial import commercial
from buildings.park import park
from buildings.road import road




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
        self.screen = screen
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
    
    def main(self):
        pygame.display.set_caption("Freeplay Game")
        clock = pygame.time.Clock()
        show_tutorial = False

        while True:
            self.screen.fill(WHITE)
            self.map.draw()
            self.draw_stats()            
            buttons = self.draw_building_buttons()

            font = pygame.font.SysFont("Arial", 18)
            draw_legend(self.screen, font)

            if self.message_timer > 0:
                font = pygame.font.SysFont("Arial", 20)
                msg_surface = font.render(self.message, True, RED)
                self.screen.blit(msg_surface, (10, STATS_HEIGHT + BUTTON_HEIGHT + 15))
                self.message_timer -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if pos[1] < UI_HEIGHT:
                        if self.handle_button_click(pos, buttons):
                            continue
                    if self.demolish_mode:
                        success, msg = self.demolish_building(pos)
                        if success:
                            self.turn += 1
                            self.next_turn()
                        self.show_message(msg)
                    else:
                        success, msg = self.place_building(pos)
                        if success:
                            self.turn += 1
                            self.next_turn()
                        self.show_message(msg)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key == pygame.K_h:
                        show_tutorial = not show_tutorial
                        if show_tutorial:
                            show_legend_and_tutorial(self.screen, "freeplay")

                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #         pygame.quit()
                #         return

            if self.is_game_over():
                #from mainMenu import main_menu
                from ui_utils import get_player_name
                from highscore import save_highscore

                font = pygame.font.SysFont("Arial", 40)
                label = font.render("Game Over: 20 turns of loss", True, RED)
                self.screen.blit(label, (100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)

                name = get_player_name(self.screen)
                if name:
                    save_highscore(name, self.score, "Freeplay")

                #main_menu()
                return


            pygame.display.flip()
            clock.tick(30)

    def handle_button_click(self, pos, buttons):
        for option, rect in buttons.items():
            if rect.collidepoint(pos):
                if option == "D":
                    self.demolish_mode = not self.demolish_mode
                    self.show_message("Demolish mode " + ("ON" if self.demolish_mode else "OFF"))
                elif option == "Save":
                    self.save_game()
                elif option == "Menu":
                    from mainMenu import main_menu
                    main_menu()
                else:
                    self.selected_building = option
                    self.demolish_mode = False
                    self.show_message(f"Selected: {option}")
                return True
        return False

    def draw_stats(self):
        font = pygame.font.SysFont("Arial", 20)
        profit, upkeep = self.calculate_profit_and_upkeep()
        net = profit - upkeep
        mode = "Demolish" if self.demolish_mode else self.selected_building
        stats = f"Turn: {self.turn} | Score: {self.score} | Profit: {profit} | Upkeep: {upkeep} | Net: {net} | Mode: {mode}"

        self.screen.fill(WHITE, (0, 0, SCREEN_WIDTH, STATS_HEIGHT))
        label = font.render(stats, True, BLACK)
        self.screen.blit(label, (10, BUTTON_HEIGHT + 10))

        # Legend displayed left-to-right
        legend_items_row1 = [("R", "Residential"), ("I", "Industry"), ("C", "Commercial")]
        legend_items_row2 = [("O", "Park"), ("*", "Road")]

        font_small = pygame.font.SysFont("Arial", 18)
        x_start = self.screen.get_width() - 400
        y_start = 10
        spacing = 130

        for i, (symbol, label) in enumerate(legend_items_row1):
            text = font_small.render(f"{symbol}: {label}", True, BLACK)
            self.screen.blit(text, (x_start + i * spacing, y_start))

        for i, (symbol, label) in enumerate(legend_items_row2):
            text = font_small.render(f"{symbol}: {label}", True, BLACK)
            self.screen.blit(text, (x_start + i * spacing, y_start + 22))

        


    def draw_building_buttons(self):
        font = pygame.font.SysFont("Arial", 20)
        buttons = {}
        x_offset = BUTTON_MARGIN

        for option in BUILDING_OPTIONS:
            color = GRAY
            if option == self.selected_building and not self.demolish_mode:
                color = BUILDING_COLORS.get(option, GRAY)
            elif option == "D" and self.demolish_mode:
                color = BUILDING_COLORS["D"]
            elif option in ["Save", "Menu"]:
                color = BUILDING_COLORS.get(option, GRAY)

            rect = pygame.Rect(x_offset, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
            # pygame.draw.rect(self.screen, color, rect)
            # pygame.draw.rect(self.screen, BLACK, rect, 2)

            label_text = option if option != "D" else "Demolish"
            label = font.render(label_text, True, BLACK)
            label_rect = label.get_rect(center=rect.center)
            # self.screen.blit(label, label_rect)
            draw_button(self.screen, rect, label_text, font, color)


            buttons[option] = rect
            x_offset += BUTTON_WIDTH + BUTTON_MARGIN

        return buttons

    def get_bounds(self):
        if not self.map.grid:
            return 0, self.map.grid_size - 1, 0, self.map.grid_size - 1
        rows = [pos[0] for pos in self.map.grid.keys()]
        cols = [pos[1] for pos in self.map.grid.keys()]
        return min(rows), max(rows), min(cols), max(cols)

    def get_adjacent(self, row, col): #i dont know if this is necessary
        adj = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dy, col + dx
            adj.append(self.map.grid.get((r, c), "."))
        return adj
    
    def get_adjacent_buildings_counts(self, row, col):
        counts = {}
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = self.map.grid.get((row + dy, col + dx))
            if neighbor:
                key = getattr(neighbor, "type_identifier", None)
                if key:
                    counts[key] = counts.get(key, 0) + 1
        return counts


    def calculate_profit_and_upkeep(self):
        profit = 0
        upkeep = 0
        visited = set()  # Shared set for cluster detection

        for (row, col), building in self.map.grid.items():
            if building.type_identifier == "R":
                if (row, col) not in visited:
                    p, u = building.calculate_profit_and_upkeep(self.map.grid, row, col, mode="freeplay", visited=visited)
                    profit += p
                    upkeep += u
            else:
                p, u = building.calculate_profit_and_upkeep(self.map.grid, row, col, mode="freeplay")
                profit += p
                upkeep += u

        return profit, upkeep





    def calculate_score(self):
        score = 0
        min_row, max_row, min_col, max_col = self.get_bounds()

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                building = self.map.grid.get((row, col))
                if building:
                    adjacent_buildings = self.get_adjacent_buildings_counts(row, col)
                    building_score = building.score(self.map.grid, row, col, mode="freeplay")
                    if isinstance(building_score, tuple):
                        profit, upkeep = building_score
                        score += profit - upkeep
                    else:
                        score += building_score

        return score


    def place_building(self, pos):
        if self.demolish_mode:
            return False, "Cannot place building in demolish mode."

        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size
        if row < 0 or col < 0 or row >= self.map.grid_size or col >= self.map.grid_size:
            return False, "Invalid placement."

        if (row, col) in self.map.grid:
            return False, "Cell already occupied."

        building_class_map = {
            "R": residential,
            "I": industry,
            "C": commercial,
            "O": park,
            "*": road
        }
        if self.selected_building not in building_class_map:
            return False, f"Unknown building type: {self.selected_building}"

        building_instance = building_class_map[self.selected_building]()
        building_instance.row = row
        building_instance.col = col

        self.map.grid[(row, col)] = building_instance

        if self.map.is_on_border(row, col):
            self.map.expand_grid()

        self.score = self.calculate_score()
        self.map.first_turn = False
        return True, "Building placed."

    
    def demolish_building(self, pos):
        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size
        if row < 0 or col < 0 or row >= self.map.grid_size or col >= self.map.grid_size:
            return False, "Invalid placement."
        if (row, col) in self.map.grid:
            del self.map.grid[(row, col)]
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
            'score': self.score,
            'grid_size': self.map.grid_size,
            'tile_size': self.map.tile_size,
            'left_margin': self.map.left_margin,
            'top_margin': self.map.top_margin,
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
        self.map.grid_size = data.get('grid_size', 5)  # default fallback 5
        self.map.tile_size = data.get('tile_size', 64) # or your default tile size
        self.map.left_margin = data.get('left_margin', 0)
        self.map.top_margin = data.get('top_margin', 0)

    def show_message(self, msg, duration=120):
        self.message = msg
        self.message_timer = duration
    def run(self):
        self.main()

def draw_legend(screen, font):
    # Smaller legend box
    legend_rect = pygame.Rect(10, 520, 300, 50)
    pygame.draw.rect(screen, (240, 240, 240), legend_rect)
    pygame.draw.rect(screen, (0, 0, 0), legend_rect, 2)  # border

    # Display one line of legend text
    legend_text = "Press H to see more details"
    text_surf = font.render(legend_text, True, (0, 0, 0))
    screen.blit(text_surf, (legend_rect.x + 10, legend_rect.y + 15))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    game = FreePlayGame(screen)
    game.main()



