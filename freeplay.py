# freeplay.py - Free play mode for the city-building game
import pygame
import pickle
import importlib
from mapv2 import Map
from tutorial import show_legend_and_tutorial
from buildings.residential import residential
from buildings.industry import industry
from buildings.commercial import commercial
from buildings.park import park
from buildings.road import road
from highscore import save_highscore
from ui_utils import get_player_name
from ui_utils import draw_full_top_ui
from economy import GameEconomy  # Import GameEconomy for integrated logic

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BUILDING_OPTIONS = ["R", "I", "C", "O", "*"]
CONTROL_OPTIONS = ["Demolish", "Save", "Menu"]

BUILDING_COLORS = {
    "R": (255, 150, 150),
    "I": (200, 200, 100),
    "C": (150, 200, 255),
    "O": (180, 255, 180),
    "*": (150, 150, 150),
    "Demolish": (255, 0, 0),
    "Save": (100, 255, 100),
    "Menu": (255, 200, 0),
}

LEGEND_ITEMS_ROW1 = [("R", "Residential"), ("I", "Industry"), ("C", "Commercial")]
LEGEND_ITEMS_ROW2 = [("O", "Park"), ("*", "Road")]

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

class FreePlayGame:
    def __init__(self, screen):
        self.map = Map("freeplay", grid_size=5, screen=screen)
        self.map.screen = screen
        self.map.initialize_screen()

        self.economy = GameEconomy(self.map, mode="freeplay")  # Use integrated economy and scoring
        self.score = self.economy.score

        self.turn = 0
        self.loss_turns = 0
        self.max_loss_turns = 20

        self.selected_building = "R"
        self.demolish_mode = False
        self.message = ""
        self.message_timer = 0

    def show_message(self, msg, duration=120):
        self.message = msg
        self.message_timer = duration

    def place_building(self, pos):
        if self.demolish_mode:
            return False, "Cannot place building in demolish mode."

        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size

        if (row, col) in self.map.grid:
            return False, "Cell already occupied."

        success, msg = self.economy.place_building((col, row), self.selected_building)
        if success:
            if self.map.is_on_border(row, col):
                self.map.expand_grid()
            self.turn += 1
            self.score = self.economy.score
            self.map.first_turn = False
        return success, msg

    def demolish_building(self, pos):
        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size

        if (row, col) in self.map.grid:
            del self.map.grid[(row, col)]
            self.score = self.economy.calculate_total_score()
            return True, "Building demolished."
        return False, "No building to demolish."

    def update_loss_turns(self):
        profit, upkeep = self.economy.calculate_freeplay_income()
        if profit < upkeep:
            self.loss_turns += 1
        else:
            self.loss_turns = 0

    def is_game_over(self):
        return self.loss_turns >= self.max_loss_turns

    def save_game(self):
        import os
        filename = self.get_filename_gui()
        if not filename.lower().endswith(".pkl"):
            filename += ".pkl"

        folder = "saves"
        if not os.path.exists(folder):
            os.makedirs(folder)

        full_path = os.path.join(folder, filename)

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
        with open(full_path, 'wb') as f:
            pickle.dump(data, f)

        print(f"Game saved as {full_path}")

    def get_filename_gui(self):
        import pygame
        input_text = ''
        input_active = True
        clock = pygame.time.Clock()
        input_box = pygame.Rect(300, 300, 400, 50)
        color_inactive = pygame.Color('gray')
        color_active = pygame.Color('white')
        color = color_active
        font = pygame.font.SysFont(None, 36)

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return input_text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            self.map.screen.fill((30, 30, 30))
            txt_surface = font.render("Enter save filename: " + input_text, True, color)
            width = max(400, txt_surface.get_width() + 10)
            input_box.w = width
            self.map.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))
            pygame.draw.rect(self.map.screen, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

    def load_data(self, data):
        self.map.grid = data.get('grid', {})
        self.turn = data.get('turn', 0)
        self.loss_turns = data.get('loss_turns', 0)
        self.score = data.get('score', 0)
        self.map.grid_size = data.get('grid_size', self.map.grid_size)
        self.map.tile_size = data.get('tile_size', self.map.tile_size)
        self.map.left_margin = data.get('left_margin', self.map.left_margin)
        self.map.top_margin = data.get('top_margin', self.map.top_margin)

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 20)

        while True:
            screen = self.map.screen
            screen.fill(WHITE)
            self.map.draw()

            buttons = draw_full_top_ui(screen, self, self.message, demolish_mode=self.demolish_mode)
            if self.message_timer > 0:
                self.message_timer -= 1
            else:
                self.message = ""

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
                    elif buttons["Save"].collidepoint(pos):
                        self.save_game()
                        self.show_message("Game Saved")
                    elif buttons["Demolish"].collidepoint(pos):
                        self.demolish_mode = not self.demolish_mode
                        self.show_message("Demolish Mode " + ("ON" if self.demolish_mode else "OFF"))
                    else:
                        for option in BUILDING_OPTIONS:
                            if buttons[option].collidepoint(pos):
                                self.selected_building = option
                                self.demolish_mode = False
                                self.show_message(f"Selected: {option}")
                                break
                        else:
                            if self.demolish_mode:
                                success, msg = self.demolish_building(pos)
                            else:
                                success, msg = self.place_building(pos)
                            self.show_message(msg)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key == pygame.K_h:
                        show_legend_and_tutorial(self.map.screen, "freeplay")

            self.update_loss_turns()
            profit, upkeep = self.economy.calculate_freeplay_income()
            profit_text = font.render(f"Profit: {profit}", True, (0, 128, 0))
            upkeep_text = font.render(f"Upkeep: {upkeep}", True, (128, 0, 0))

            screen.blit(profit_text, (10, SCREEN_HEIGHT - 60))
            screen.blit(upkeep_text, (10, SCREEN_HEIGHT - 30))


            if self.is_game_over():
                font = pygame.font.SysFont("Arial", 40)
                label = font.render("Game Over: 20 turns of loss", True, RED)
                self.map.screen.blit(label, (100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)

                name = get_player_name(self.map.screen)
                if name:
                    save_highscore(name, self.score, "Freeplay")
                return

            pygame.display.flip()
            clock.tick(30)

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    game = FreePlayGame(screen)
    game.run()

if __name__ == "__main__":
    main()
