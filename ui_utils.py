import pygame

def draw_button(screen, rect, label, font, color=(200, 200, 200), border_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, border_color, rect, 2)
    text_surface = font.render(label, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

import pygame

def get_player_name(screen):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 36)
    input_box = pygame.Rect(100, 200, 400, 50)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')
    color = color_inactive

    active = True
    text = ""
    done = False
    clock = pygame.time.Clock()

    while not done:
        screen.fill((0, 0, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Cancelled
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.strip():
                            return text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 15:
                            text += event.unicode

        txt_surface = font.render(text, True, (255, 255, 255))
        width = max(400, txt_surface.get_width() + 10)
        input_box.w = width

        screen.blit(font.render("Enter Your Name:", True, (255, 255, 0)), (100, 130))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color_active if active else color_inactive, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
