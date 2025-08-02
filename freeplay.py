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
from scoring import get_connected_neighbors

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
        self.turn = 0
        self.loss_turns = 0
        self.max_loss_turns = 20
        self.score = 0
        self.selected_building = "R"
        self.demolish_mode = False
        self.message = ""
        self.message_timer = 0

    def calculate_profit_and_upkeep(self):
        profit = 0
        upkeep = 0
        for (row, col), building in self.map.grid.items():
            p, u = building.calculate_profit_and_upkeep(self.map.grid, row, col)
            profit += p
            upkeep += u
        return profit, upkeep

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

        building_class_map = {
            "R": residential,
            "I": industry,
            "C": commercial,
            "O": park,
            "*": road,
        }
        building_instance = building_class_map[self.selected_building]()
        self.map.grid[(row, col)] = building_instance

        if self.map.is_on_border(row, col):
            self.map.expand_grid()

        self.score = self.calculate_total_score()
        self.map.first_turn = False
        return True, "Building placed."

    def demolish_building(self, pos):
        x, y = pos
        row = (y - self.map.top_margin) // self.map.tile_size
        col = (x - self.map.left_margin) // self.map.tile_size
        if (row, col) in self.map.grid:
            del self.map.grid[(row, col)]
            self.score = self.calculate_total_score()
            return True, "Building demolished."
        return False, "No building to demolish."
    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 20)

        while True:
            screen = self.map.screen
            screen.fill((255, 255, 255))
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
                    # Handle control buttons
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
                        # Building buttons
                        for option in ["R","I","C","O","*"]:
                            if buttons[option].collidepoint(pos):
                                self.selected_building = option
                                self.demolish_mode = False
                                self.show_message(f"Selected: {option}")
                                break
                        else:
                            # Place or demolish
                            if self.demolish_mode:
                                success, msg = self.demolish_building(pos)

                            else:
                                success, msg = self.place_building(pos)
                                if success:
                                    self.turn += 1 
                            self.show_message(msg)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key == pygame.K_h:
                        show_legend_and_tutorial(self.screen, "freeplay")


            if self.is_game_over():
                font = pygame.font.SysFont("Arial", 40)
                label = font.render("Game Over: 20 turns of loss", True, RED)
                self.screen.blit(label, (100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)

                name = get_player_name(self.screen)
                if name:
                    save_highscore(name, self.score, "Freeplay")
                return

            pygame.display.flip()
            clock.tick(30)

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
        return True

def main():
    pygame.init()
    # screen = pygame.display.set_mode((1280, 800), pygame.NOFRAME) 
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    game = FreePlayGame(screen)
    game.run()

if __name__ == "__main__":
    main()


