import pygame
from ui.slider import Slider
from buttons import Button
from settings import FONT_PATH


# ==============================================================================
# ============================ ЕКРАН НАЛАШТУВАНЬ ГРИ ===========================
# ==============================================================================
class SettingsMenu:
    def __init__(self, initial_volume, initial_keys, min_keys, max_keys, on_change, on_back):
        self.volume = initial_volume
        self.keys_count = initial_keys
        self.on_change_cb = on_change
        self.on_back_cb = on_back

        # Використання нового шрифту copperplate_light для меню
        try:
            self.font = pygame.font.Font(FONT_PATH, 14)
            self.title_font = pygame.font.Font(FONT_PATH, 24)
        except IOError:
            self.font = pygame.font.SysFont("Arial", 14, bold=True)
            self.title_font = pygame.font.SysFont("Arial", 24, bold=True)

        self.back_btn = Button("<- BACK", 20, 20, 100, 40)

        self.vol_slider = Slider(250, 140, 300, 0.00, 1.00, initial_volume, "VOLUME", is_int=False)
        self.keys_slider = Slider(250, 240, 300, min_keys, max_keys, initial_keys, "KEYS COUNT", is_int=True)

        self.vol_slider.set_on_change(self._on_volume)
        self.keys_slider.set_on_change(self._on_keys)

    def _on_volume(self, val):
        self.volume = val
        self.on_change_cb(self.volume, self.keys_count)

    def _on_keys(self, val):
        self.keys_count = int(val)
        self.on_change_cb(self.volume, self.keys_count)

    def draw(self, screen):
        title_surf = self.title_font.render("SETTINGS", True, (50, 50, 50))
        screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 40))

        self.back_btn.draw(screen)
        self.vol_slider.draw(screen, self.font)
        self.keys_slider.draw(screen, self.font)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.back_btn.update(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.collidepoint(event.pos):
                self.back_btn.flash_timer = 1.5
                if self.on_back_cb:
                    self.on_back_cb()
                    return

        self.vol_slider.handle_event(event)
        self.keys_slider.handle_event(event)
