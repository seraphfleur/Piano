import pygame
from settings import FONT_PATH


# ==============================================================================
# ======================== УНІВЕРСАЛЬНИЙ КОМПОНЕНТ СЛАЙДЕРА ====================
# ==============================================================================
class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label="", is_int=False):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.is_int = is_int

        self.on_change_cb = None
        self.is_dragging = False

        self.track_rect = pygame.Rect(x, y + 10, width, 6)
        self.handle_radius = 9
        self.update_handle_pos()

    def update_handle_pos(self):
        val_range = self.max_val - self.min_val
        fraction = (self.value - self.min_val) / val_range if val_range != 0 else 0
        self.handle_x = self.x + int(fraction * self.width)
        self.handle_y = self.y + 13

    def set_on_change(self, cb):
        self.on_change_cb = cb

    def draw(self, screen, font=None):
        # Скляний напівпрозорий трек повзунка
        track_surf = pygame.Surface((self.width, 6), pygame.SRCALPHA)
        pygame.draw.rect(track_surf, (255, 255, 255, 100), (0, 0, self.width, 6), border_radius=3)
        screen.blit(track_surf, self.track_rect.topleft)
        pygame.draw.rect(screen, (0, 0, 0, 30), self.track_rect, 1, border_radius=3)

        # Елегантна скляна ручка повзунка
        handle_surf = pygame.Surface((self.handle_radius * 2, self.handle_radius * 2), pygame.SRCALPHA)
        h_alpha = 240 if self.is_dragging else 180
        pygame.draw.circle(handle_surf, (255, 255, 255, h_alpha), (self.handle_radius, self.handle_radius),
                           self.handle_radius)
        pygame.draw.circle(handle_surf, (255, 255, 255, 255), (self.handle_radius, self.handle_radius),
                           self.handle_radius, 2)
        screen.blit(handle_surf, (self.handle_x - self.handle_radius, self.handle_y - self.handle_radius))

        # Тонкий контур для тіні ручки
        pygame.draw.circle(screen, (0, 0, 0, 50), (self.handle_x, self.handle_y), self.handle_radius, 1)

        if font:
            display_val = int(self.value) if self.is_int else f"{int(self.value * 100)}%"
            text_surf = font.render(f"{self.label}: {display_val}", True, (50, 50, 50))
            screen.blit(text_surf, (self.x, self.y - 15))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            distance = ((event.pos[0] - self.handle_x) ** 2 + (event.pos[1] - self.handle_y) ** 2) ** 0.5
            if distance <= self.handle_radius + 5:
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            mouse_x = max(self.x, min(event.pos[0], self.x + self.width))
            fraction = (mouse_x - self.x) / self.width
            new_val = self.min_val + fraction * (self.max_val - self.min_val)
            if self.is_int:
                new_val = round(new_val)
            else:
                new_val = round(new_val, 2)
            if new_val != self.value:
                self.value = new_val
                self.update_handle_pos()
                if self.on_change_cb:
                    self.on_change_cb(self.value)