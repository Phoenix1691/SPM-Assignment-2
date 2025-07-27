import pygame

def draw_button(screen, rect, label, font, color=(200, 200, 200), border_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, border_color, rect, 2)
    text_surface = font.render(label, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)