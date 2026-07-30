import pygame
from settings import FONT_PATH
from effects import draw_glass_rect


# ==============================================================================
# =========================== СТРУКТУРА КНОПКИ МЕНЮ ============================
# ==============================================================================
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

        # Спроба імпортувати кастомний шрифт
        try:
            self.font = pygame.font.Font(FONT_PATH, 14)
        except IOError:
            self.font = pygame.font.SysFont("Arial", 14, bold=True)

        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        # Зміна прозорості та відтінку при наведенні миші
        base_color = (255, 255, 255) if self.is_hovered else (245, 245, 250)
        alpha = 210 if self.is_hovered else 150

        # Малюємо матове скло для кнопки
        draw_glass_rect(screen, self.rect, base_color, alpha, (255, 255, 255), 230, radius=10, border_width=2)
        draw_glass_rect(screen, self.rect, (0, 0, 0), 0, (0, 0, 0), 70, radius=10, border_width=1)

        # Рендер тексту всередині кнопки
        text_surf = self.font.render(self.text, True, (45, 45, 45))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
