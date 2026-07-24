import pygame
from settings import BLACK, GREY
from effects import draw_button_flash

# ==============================================================================
# =========================== СТРУКТУРА КНОПКИ МЕНЮ ============================
# ==============================================================================
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Arial", 20)
        self.is_hovered = False
        self.flash_timer = 0 # Таймер для тривалості спалаху

    def update(self, mouse_pos):
        # Перевіряємо, чи наведена миша на кнопку
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        # Зменшуємо таймер спалаху з часом
        if self.flash_timer > 0:
            self.flash_timer -= 0.1

    def draw(self, screen):
        # Якщо миша наведена — кнопка стає трохи світлішою
        bg_color = (230, 230, 230) if self.is_hovered else GREY
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        
        # Викликаємо ефект спалаху
        draw_button_flash(screen, self.rect, self.flash_timer)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
