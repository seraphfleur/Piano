import pygame
from buttons import Button
from ui.slider import Slider
from settings import FONT_PATH, WINDOW_WIDTH


class SettingsMenu:
    def __init__(self, initial_volume, initial_keys, initial_random, min_keys, max_keys, on_change, on_toggle_random, on_back):
        self.volume = initial_volume
        self.keys_count = initial_keys
        self.is_random = initial_random

        self.on_change = on_change
        self.on_toggle_random = on_toggle_random
        self.on_back = on_back

        self.back_btn = Button("<- НАЗАД", 20, 20, 110, 40)
        self.vol_slider = Slider(200, 150, 400, 20, 0.0, 1.0, self.volume, is_int=False)
        self.keys_slider = Slider(200, 240, 400, 20, min_keys, max_keys, self.keys_count, is_int=True)
        self.random_btn = Button("ВИПАДКОВІ ЗВУКИ", 180, 310, 210, 40)

        try:
            self.font = pygame.font.Font(FONT_PATH, 16)
            self.title_font = pygame.font.Font(FONT_PATH, 22)
        except IOError:
            self.font = pygame.font.SysFont("Arial", 16, bold=True)
            self.title_font = pygame.font.SysFont("Arial", 22, bold=True)

        # Статичний заголовок
        self._title_surf = self.title_font.render("НАЛАШТУВАННЯ", True, (35, 35, 35))
        self._title_pos = (WINDOW_WIDTH // 2 - self._title_surf.get_width() // 2, 35)

    def handle_event(self, e):
        mouse_pos = pygame.mouse.get_pos()
        self.back_btn.update(mouse_pos)
        self.random_btn.update(mouse_pos)

        vol_changed = self.vol_slider.handle_event(e)
        keys_changed = self.keys_slider.handle_event(e)

        if vol_changed or keys_changed:
            self.volume = self.vol_slider.val
            self.keys_count = self.keys_slider.val
            if self.on_change:
                self.on_change(self.volume, self.keys_count)

        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.collidepoint(e.pos):
                self.on_back()
            elif self.random_btn.collidepoint(e.pos):
                self.is_random = not self.is_random
                if self.on_toggle_random:
                    self.on_toggle_random(self.is_random)

    def draw(self, screen):
        self.back_btn.draw(screen)
        screen.blit(self._title_surf, self._title_pos)

        # Гучність
        vol_surf = self.font.render(f"ГУЧНІСТЬ: {int(self.volume * 100)}%", True, (35, 35, 35))
        screen.blit(vol_surf, (200, 120))
        self.vol_slider.draw(screen)

        # Кількість клавіш
        keys_surf = self.font.render(f"КІЛЬКІСТЬ КЛАВІШ: {self.keys_count}", True, (35, 35, 35))
        screen.blit(keys_surf, (200, 210))
        self.keys_slider.draw(screen)

        # Кнопка та статус випадкових звуків
        self.random_btn.draw(screen)
        status_text = f"СТАН: {'УВІМК' if self.is_random else 'ВИМК'}"
        status_color = (27, 94, 32) if self.is_random else (35, 35, 35)
        status_surf = self.font.render(status_text, True, status_color)
        screen.blit(status_surf, (410, 320))
