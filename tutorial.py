import pygame

def show_legend_and_tutorial(screen, mode):
    screen.fill((30, 30, 30))
    font_title = pygame.font.SysFont("Arial", 36)
    font = pygame.font.SysFont("Arial", 22)

    # Left Column (Legend + Scoring)
    legend = [
        "LEGEND:",
        "R - Residential",
        "I - Industry",
        "C - Commercial",
        "O - Park",
        "* - Road",
        ""
    ]

    scoring = [
        "SCORING MECHANICS:",
        "Residential (R):",
        "  - If next to Industry (I): 1 point total",
        "  - Else: 1 point per adjacent R or C,",
        "    2 points per adjacent Park (O)",
        "",
        "Industry (I):",
        "  - 1 point per Industry in city",
        "  - Generates 1 coin per adjacent Residential",
        "",
        "Commercial (C):",
        "  - 1 point per adjacent Commercial",
        "  - Generates 1 coin per adjacent Residential",
        "",
        "Park (O):",
        "  - 1 point per adjacent Park",
        "",
        "Road (*):",
        "  - 1 point per connected Road in same row",
        ""
    ]

    # Right Column (Mode-specific tutorial)
    if mode == "arcade":
        tutorial = [
            "ARCADE MODE TUTORIAL:",
            "• Start with 16 coins. Each building costs 1 coin.",
            "• Each turn, choose one of two random buildings.",
            "• First building can go anywhere. Others must be adjacent.",
            "• Unused building is discarded.",
            "• Goal: maximize your city score!"
        ]
    elif mode == "freeplay":
        tutorial = [
            "FREE PLAY MODE TUTORIAL:",
            "• Unlimited coins. Start with a 5x5 grid.",
            "• Place buildings freely. Border placement expands the grid.",
            "• Each border placement adds 5 rows/columns.",
            "• Scoring is same as arcade mode.",
            "",
            "INCOME & UPKEEP:",
            "Residential (R): +1/turn, -1/turn for clusters",
            "Industry (I): +2/turn, -1 upkeep",
            "Commercial (C): +3/turn, -2 upkeep",
            "Park (O): -1 upkeep",
            "Road (*): -1 upkeep if unconnected"
        ]
    else:
        tutorial = ["Invalid game mode!"]

    # Draw left column
    y_left = 20
    x_left = 40
    for line in legend + scoring:
        is_header = line.endswith(":")
        text = font_title.render(line, True, (255, 255, 255)) if is_header else font.render(line, True, (255, 255, 255))
        screen.blit(text, (x_left, y_left))
        y_left += 32

    # Draw right column
    y_right = 20
    screen_width = screen.get_width()
    x_right = screen_width // 2 + 20
    for line in tutorial:
        is_header = line.endswith(":") or line.endswith("TUTORIAL:")
        text = font_title.render(line, True, (255, 255, 255)) if is_header else font.render(line, True, (255, 255, 255))
        screen.blit(text, (x_right, y_right))
        y_right += 32

    # Footer
    footer = font.render("Press any key to return...", True, (200, 200, 200))
    screen.blit(footer, (screen_width // 2 - footer.get_width() // 2, screen.get_height() - 50))

    pygame.display.flip()

    # Wait for any key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
