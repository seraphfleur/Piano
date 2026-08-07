import pygame
from settings import FONT_PATH
from effects import draw_glass_rect

_SHARED_FONT = None


def get_button_font():
    global _SHARED_FONT
    if _SHARED_FONT is None:
        try:
            _SHARED_FONT = pygame.font.Font(FONT_PATH, 14)
        except IOError:
            _SHARED_FONT = pygame.font.SysFont("Arial", 14, bold=True)
    return _SHARED_FONT


class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = get_button_font()
        self.is_hovered = False

        # Попередній рендеринг тексту
        self.text = text
        self._cached_text_surf = self.font.render(self.text, True, (45, 45, 45))
        self._cached_text_rect = self._cached_text_surf.get_rect(center=self.rect.center)

    def set_text(self, text):
        if self.text != text:
            self.text = text
            self._cached_text_surf = self.font.render(self.text, True, (45, 45, 45))
            self._cached_text_rect = self._cached_text_surf.get_rect(center=self.rect.center)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        base_color = (255, 255, 255) if self.is_hovered else (245, 245, 250)
        alpha = 210 if self.is_hovered else 150

        draw_glass_rect(screen, self.rect, base_color, alpha, (255, 255, 255), 230, radius=10, border_width=2)
        draw_glass_rect(screen, self.rect, (0, 0, 0), 0, (0, 0, 0), 70, radius=10, border_width=1)

        # Малюємо вже підготовлений текст
        screen.blit(self._cached_text_surf, self._cached_text_rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
