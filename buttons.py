import pygame
from settings import BLACK, GREY


# ==============================================================================
# =========================== СТРУКТУРА КНОПКИ МЕНЮ ============================
# ==============================================================================
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)

        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)