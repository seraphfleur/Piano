import pygame
from pygame import *
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, keys_list, KEYS, FPS
from keys import create_key_rects, draw_keys
from sounds import sounds
from buttons import Button
from ui.settings_menu import SettingsMenu

# ==============================================================================
# ============================ СТАРТ ПРОЄКТУ ТА ВІКНО ===========================
# ==============================================================================
init()
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Piano Game")
clock = time.Clock()
running = True

# ==============================================================================
# ======================== ЗАВАНТАЖЕННЯ ГРАФІЧНИХ АСЕТІВ =======================
# ==============================================================================
try:
    BACKGROUND_IMG = image.load('assets/images/background.png')
    BACKGROUND_IMG = transform.scale(BACKGROUND_IMG, (WINDOW_WIDTH, WINDOW_HEIGHT))
except error:
    BACKGROUND_IMG = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    BACKGROUND_IMG.fill((230, 233, 240))

try:
    LOGO_IMG = image.load('assets/images/logo.png')
    LOGO_IMG = transform.scale(LOGO_IMG, (220, 60))
except error:
    LOGO_IMG = None

# ==============================================================================
# ==================== СТАН ЕКРАНУ ТА НАЛАШТУВАННЯ ПО УМОЛЧАННЮ =================
# ==============================================================================
current_screen = "main"
current_volume = 0.7
current_keys_count = 7

# ==============================================================================
# =========================== ІНІЦІАЛІЗАЦІЯ ОБ'ЄКТІВ ===========================
# ==============================================================================
pressed = set()
key_rects = create_key_rects(current_keys_count)
settings_btn = Button("Settings", 20, 20, 100, 40)
settings_menu = None

# Додано базовий масштаб 'scale' для анімації стискання клавіш
key_anims = [{'color': [255, 255, 255], 'offset': 0.0, 'pulse': 0.0, 'scale': 1.0} for _ in range(current_keys_count)]

for snd in sounds.values():
    if snd:
        snd.set_volume(current_volume)


# ==============================================================================
# =========================== ФУНКЦІЇ КЕРУВАННЯ СТАНАМИ ========================
# ==============================================================================
def apply_settings(volume, key_count):
    global current_volume, current_keys_count, key_rects, pressed, key_anims
    current_volume = volume
    current_keys_count = key_count

    for snd in sounds.values():
        if snd:
            snd.set_volume(current_volume)

    key_rects = create_key_rects(current_keys_count)
    pressed = {idx for idx in pressed if idx < current_keys_count}
    key_anims = [{'color': [255, 255, 255], 'offset': 0.0, 'pulse': 0.0, 'scale': 1.0} for _ in
                 range(current_keys_count)]


def _back_to_main():
    global current_screen
    current_screen = "main"


# ==============================================================================
# ============================ ГОЛОВНИЙ ЦИКЛ ГРИ ===============================
# ==============================================================================
while running:
    clock.tick(FPS)
    mouse_pos = mouse.get_pos()

    # --------------------------- ОБРОБКА ПОДІЙ СИСТЕМИ ------------------------
    events = event.get()
    for e in events:
        if e.type == QUIT:
            running = False

        if current_screen == "settings":
            if settings_menu:
                settings_menu.handle_event(e)
        else:
            settings_btn.update(mouse_pos)

            # --- Механіка клавіатури ---
            if e.type == KEYDOWN:
                k = key.name(e.key)
                if k in keys_list:
                    idx = keys_list.index(k)
                    if idx < current_keys_count:
                        if idx not in pressed:
                            key_anims[idx]['pulse'] = 1.5
                        if sounds[k]:
                            sounds[k].play()
                        pressed.add(idx)

            if e.type == KEYUP:
                k = key.name(e.key)
                if k in keys_list:
                    idx = keys_list.index(k)
                    pressed.discard(idx)

            # --- Механіка миші ---
            if e.type == MOUSEBUTTONDOWN:
                if settings_btn.collidepoint(e.pos):
                    # Ефект спалаху для кнопки налаштувань видалено
                    current_screen = "settings"
                    settings_menu = SettingsMenu(
                        initial_volume=current_volume,
                        initial_keys=current_keys_count,
                        min_keys=1,
                        max_keys=len(KEYS),
                        on_change=apply_settings,
                        on_back=_back_to_main
                    )

                for i, r in enumerate(key_rects):
                    if r.collidepoint(e.pos):
                        k = keys_list[i]
                        if i not in pressed:
                            key_anims[i]['pulse'] = 1.5
                        if sounds[k]:
                            sounds[k].play()
                        pressed.add(i)

            if e.type == MOUSEBUTTONUP:
                for i, r in enumerate(key_rects):
                    if i in pressed and r.collidepoint(e.pos):
                        pressed.remove(i)

    # ----------------------- ОБЧИСЛЕННЯ ПЛАВНИХ АНІМАЦІЙ --------------------
    if current_screen == "main":
        for i in range(current_keys_count):
            is_pressed = i in pressed

            # Ефекти натискання: затемнення кольору до матового сірого та зменшення масштабу до 0.94
            target_color = [165, 165, 165] if is_pressed else [255, 255, 255]
            target_scale = 0.94 if is_pressed else 1.0
            target_offset = 0.0

            # Плавна лінійна інтерполяція (коефіцієнт 0.25 для м'якості анімації)
            for c_idx in range(3):
                key_anims[i]['color'][c_idx] += (target_color[c_idx] - key_anims[i]['color'][c_idx]) * 0.25
            key_anims[i]['offset'] += (target_offset - key_anims[i]['offset']) * 0.25
            key_anims[i]['scale'] += (target_scale - key_anims[i]['scale']) * 0.25

            # Плавне згасання таймера білого імпульсу (pulse)
            if key_anims[i]['pulse'] > 0:
                key_anims[i]['pulse'] -= 0.05
                if key_anims[i]['pulse'] < 0:
                    key_anims[i]['pulse'] = 0.0

    # -------------------------- ВІДМАЛЬОВКА ЕКРАНІВ ---------------------------
    screen.blit(BACKGROUND_IMG, (0, 0))

    if current_screen == "settings":
        if settings_menu:
            settings_menu.draw(screen)
    else:
        if LOGO_IMG:
            logo_x = (WINDOW_WIDTH - LOGO_IMG.get_width()) // 2
            screen.blit(LOGO_IMG, (logo_x, 25))

        draw_keys(screen, key_rects, key_anims)
        settings_btn.draw(screen)

    display.update()

quit()
