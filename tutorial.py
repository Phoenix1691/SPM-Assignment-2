import pygame

def show_legend_and_tutorial(screen):
    screen.fill((30, 30, 30))
    font_title = pygame.font.SysFont("Arial", 40)
    font = pygame.font.SysFont("Arial", 24)
    
    lines = [
        "LEGEND:",
        "R - Residential",
        "I - Industry",
        "C - Commercial",
        "O - Park",
        "* - Road",
        "",
        "SCORING MECHANICS:",
        "Residential (R):",
        "  - If next to Industry (I): 1 point total",
        "  - Else: 1 point per adjacent R or C, 2 points per adjacent Park (O)",
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
        "  - 1 point per connected Road in the same row",
        "",
        "Press any key to return..."
    ]

    y = 30
    for line in lines:
        text = font_title.render(line, True, (255, 255, 255)) if line.endswith(":") else font.render(line, True, (255, 255, 255))
        screen.blit(text, (50, y))
        y += 35

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
