# ui_utils.py - Unified UI utilities for both Free Play and Arcade mode
import pygame

# === Shared UI Colors ===
UI_BG_COLOR = (230, 230, 230)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLORS = {
    "R": (255, 180, 180),
    "I": (200, 200, 120),
    "C": (150, 200, 255),
    "O": (180, 255, 180),
    "*": (150, 150, 150),
    "Demolish": (255, 150, 150),
    "Save": (150, 255, 150),
    "Menu": (255, 220, 100),
}

LEGEND_ITEMS_ROW1 = [("R", "Residential"), ("I", "Industry"), ("C", "Commercial")]
LEGEND_ITEMS_ROW2 = [("O", "Park"), ("*", "Road")]
MODE_BAR_HEIGHT = 30
UI_BAR_HEIGHT = 75  # enough for 2 rows of buttons
MESSAGE_BAR_HEIGHT = 30     # Dedicated message bar height

def draw_button(screen, rect, label, font, color=(200,200,200), border_color=(0,0,0)):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, border_color, rect, 2)
    text_surface = font.render(label, True, (0,0,0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def get_player_name(screen):
    """Prompts the player for their name in a simple input box."""
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 36)
    input_box = pygame.Rect(100, 200, 400, 50)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')

    active = True
    text = ""
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Cancelled
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN and text.strip():
                    return text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 15:
                    text += event.unicode

        # Draw input box and text
        txt_surface = font.render(text, True, (255, 255, 255))
        input_box.w = max(400, txt_surface.get_width() + 10)

        screen.blit(font.render("Enter Your Name:", True, (255, 255, 0)), (100, 130))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color_active, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def draw_legend(screen, font, y_offset=0):
    legend_items_row1 = [("R", "Residential"), ("I", "Industry"), ("C", "Commercial")]
    legend_items_row2 = [("O", "Park"), ("*", "Road")]

    width = screen.get_width()
    x_start = width - 380
    y_start = 5 + y_offset
    spacing = 130

    # Row 1
    for i, (symbol, label) in enumerate(legend_items_row1):
        text = font.render(f"{symbol}: {label}", True, (0, 0, 0))
        screen.blit(text, (x_start + i * spacing, y_start))

    # Row 2
    for i, (symbol, label) in enumerate(legend_items_row2):
        text = font.render(f"{symbol}: {label}", True, (0, 0, 0))
        screen.blit(text, (x_start + i * spacing, y_start + 25))


def draw_full_top_ui(screen, game, message="", building_choices=None, demolish_mode=False):
    # Draws the entire top UI: mode label, stats, buttons, message bar, legend.
    # Returns the button dictionary for click detection.
    font = pygame.font.SysFont("Arial", 20)
    width = screen.get_width()

    # --- Mode Bar (top line) ---
    pygame.draw.rect(screen, (210, 210, 210), (0, 0, width, MODE_BAR_HEIGHT))
    mode_label = "Free Play" if getattr(game, "coins", None) is None else "Arcade"
    screen.blit(font.render(f"Mode: {mode_label}", True, (0,0,0)), (10, 2))

    # --- Stats Bar ---
    stats_y = MODE_BAR_HEIGHT + 5
    stats = f"Turn: {game.turn}"
    if hasattr(game, "coins"):
        stats += f"    Coins: {game.coins}"
    stats += f"    Score: {game.score}"
    pygame.draw.rect(screen, UI_BG_COLOR, (0, MODE_BAR_HEIGHT, width, UI_BAR_HEIGHT))
    screen.blit(font.render(stats, True, (0,0,0)), (10, stats_y))

    # --- Buttons ---
    button_width, button_height, spacing = 60, 30, 10
    start_x = 400
    buttons = {}

    # Row 1: Building Buttons
    options = building_choices if building_choices else ["R", "I", "C", "O", "*"]
    for i, option in enumerate(options):
        rect = pygame.Rect(start_x + i*(button_width+spacing), stats_y, button_width, button_height)
        color = BUTTON_COLORS.get(option, (200,200,200))
        draw_button(screen, rect, option, font, color)
        buttons[option] = rect

    # Row 2: Control Buttons under building buttons
    control_y = stats_y + button_height + 5  # 5px gap under first row
    demolish_rect = pygame.Rect(start_x, control_y, 90, button_height)
    save_rect = pygame.Rect(demolish_rect.right + spacing, control_y, 80, button_height)
    menu_rect = pygame.Rect(save_rect.right + spacing, control_y, 100, button_height)

    draw_button(screen, demolish_rect, "Demolish", font,
                BUTTON_COLORS["Demolish"] if demolish_mode else (255,180,180))
    draw_button(screen, save_rect, "Save", font, BUTTON_COLORS["Save"])
    draw_button(screen, menu_rect, "Main Menu", font, BUTTON_COLORS["Menu"])

    buttons.update({"Demolish": demolish_rect, "Save": save_rect, "Menu": menu_rect})

    # --- Message Bar ---
    msg_y_offset = MODE_BAR_HEIGHT + UI_BAR_HEIGHT
    pygame.draw.rect(screen, (200, 200, 200), (0, msg_y_offset, width, MESSAGE_BAR_HEIGHT))
    if message:
        msg_surface = font.render(message, True, (200, 0, 0))
        screen.blit(msg_surface, (10, msg_y_offset + 5))

    # --- Legend ---
    draw_legend(screen, font, y_offset=MODE_BAR_HEIGHT)

    return buttons
