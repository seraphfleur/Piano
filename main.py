import pygame
from pygame import *
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, keys_list, KEYS, FPS
from keys import create_key_rects, draw_keys
from buttons import Button
from ui.settings_menu import SettingsMenu

from sounds import (
    init_base_sounds,
    play_sound,
    get_active_sounds_map,
    enable_random_sounds,
    disable_random_sounds,
    update_all_volumes,
    is_random_active
)

from autoplay.midi_manager import MidiAutoplayManager
from autoplay.autoplay_menu import AutoplayMenu

init()
mixer.init()
mixer.set_num_channels(64)

current_volume = 0.7
current_keys_count = 14

init_base_sounds(current_volume)

screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Piano Game")
clock = time.Clock()
running = True

KEY_MAP = {
    K_q: "q", K_w: "w", K_e: "e", K_r: "r", K_t: "t", K_y: "y", K_u: "u",
    K_a: "a", K_s: "s", K_d: "d", K_f: "f", K_g: "g", K_h: "h", K_j: "j"
}

# Швидке завантаження зображень з сумісним форматом пікселів (.convert)
try:
    BACKGROUND_IMG = image.load('assets/images/background.png').convert()
    BACKGROUND_IMG = transform.scale(BACKGROUND_IMG, (WINDOW_WIDTH, WINDOW_HEIGHT))
except error:
    BACKGROUND_IMG = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    BACKGROUND_IMG.fill((230, 233, 240))

try:
    LOGO_IMG = image.load('assets/images/logo.png').convert_alpha()
    LOGO_IMG = transform.scale(LOGO_IMG, (220, 60))
    LOGO_X = (WINDOW_WIDTH - LOGO_IMG.get_width()) // 2
except error:
    LOGO_IMG = None

current_screen = "main"

pressed = set()
hw_pressed = set()
mouse_pressed = set()

key_rects = create_key_rects(current_keys_count)

settings_btn = Button("Налаштування", 20, 20, 140, 40)
settings_menu = None

midi_manager = MidiAutoplayManager()
autoplay_menu = None
autoplay_btn = Button("Автоплей", 540, 20, 110, 40)
stop_btn = Button("Стоп MIDI", 665, 20, 115, 40)

key_anims = [{'color': [255.0, 255.0, 255.0], 'offset': 0.0, 'pulse': 0.0, 'scale': 1.0} for _ in range(current_keys_count)]


def apply_settings(volume, key_count):
    global current_volume, current_keys_count, key_rects, pressed, hw_pressed, mouse_pressed, key_anims
    current_volume = volume
    current_keys_count = key_count

    update_all_volumes(current_volume)

    key_rects = create_key_rects(current_keys_count)
    pressed = {idx for idx in pressed if idx < current_keys_count}
    hw_pressed = {idx for idx in hw_pressed if idx < current_keys_count}
    mouse_pressed = {idx for idx in mouse_pressed if idx < current_keys_count}
    key_anims = [{'color': [255.0, 255.0, 255.0], 'offset': 0.0, 'pulse': 0.0, 'scale': 1.0} for _ in range(current_keys_count)]


def toggle_random_sounds(state):
    if state:
        enable_random_sounds(current_volume)
    else:
        disable_random_sounds()


def _back_to_main():
    global current_screen
    current_screen = "main"


while running:
    clock.tick(FPS)
    mouse_pos = mouse.get_pos()

    for e in event.get():
        if e.type == QUIT:
            running = False

        if current_screen == "autoplay_menu":
            if autoplay_menu:
                autoplay_menu.handle_event(e)
            continue

        if current_screen == "settings":
            if settings_menu:
                settings_menu.handle_event(e)
        else:
            settings_btn.update(mouse_pos)
            autoplay_btn.update(mouse_pos)
            if midi_manager.is_playing:
                stop_btn.update(mouse_pos)

            # --- КЛАВІАТУРА ---
            if e.type == KEYDOWN:
                if e.key in KEY_MAP:
                    k = KEY_MAP[e.key]
                    idx = keys_list.index(k)
                    if idx < current_keys_count:
                        if idx not in pressed:
                            key_anims[idx]['pulse'] = 1.5
                        play_sound(k)
                        hw_pressed.add(idx)
                        pressed.add(idx)

            elif e.type == KEYUP:
                if e.key in KEY_MAP:
                    k = KEY_MAP[e.key]
                    idx = keys_list.index(k)
                    hw_pressed.discard(idx)
                    if idx not in mouse_pressed:
                        pressed.discard(idx)

            # --- МИША: НАТИСКАННЯ ---
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                if settings_btn.collidepoint(e.pos):
                    current_screen = "settings"
                    settings_menu = SettingsMenu(
                        initial_volume=current_volume,
                        initial_keys=current_keys_count,
                        initial_random=is_random_active(),
                        min_keys=1,
                        max_keys=len(KEYS),
                        on_change=apply_settings,
                        on_toggle_random=toggle_random_sounds,
                        on_back=_back_to_main
                    )

                elif autoplay_btn.collidepoint(e.pos):
                    current_screen = "autoplay_menu"

                    def on_midi_select(path):
                        global current_screen
                        midi_manager.load_midi(path)
                        midi_manager.start()
                        current_screen = "main"

                    autoplay_menu = AutoplayMenu(on_midi_select, _back_to_main)

                elif midi_manager.is_playing and stop_btn.collidepoint(e.pos):
                    midi_manager.stop(pressed)

                else:
                    for i, r in enumerate(key_rects):
                        if r.collidepoint(e.pos):
                            k = keys_list[i]
                            if i not in pressed:
                                key_anims[i]['pulse'] = 1.5
                            play_sound(k)
                            mouse_pressed.add(i)
                            pressed.add(i)

            # --- МИША: ВІДПУСКАННЯ ---
            elif e.type == MOUSEBUTTONUP and e.button == 1:
                for idx in mouse_pressed:
                    if idx not in hw_pressed:
                        pressed.discard(idx)
                mouse_pressed.clear()

            # --- МИША: ПРОВЕДЕННЯ З ЗАТИСНУТОЮ КНОПКОЮ ---
            elif e.type == MOUSEMOTION and e.buttons[0]:
                hovered_idx = next((i for i, r in enumerate(key_rects) if r.collidepoint(e.pos)), None)

                if hovered_idx not in mouse_pressed:
                    for idx in mouse_pressed:
                        if idx not in hw_pressed:
                            pressed.discard(idx)
                    mouse_pressed.clear()

                    if hovered_idx is not None:
                        k = keys_list[hovered_idx]
                        if hovered_idx not in pressed:
                            key_anims[hovered_idx]['pulse'] = 1.5
                        play_sound(k)
                        mouse_pressed.add(hovered_idx)
                        pressed.add(hovered_idx)

    # Оновлення стану сцен
    if current_screen == "main":
        midi_manager.update(pressed, key_anims, get_active_sounds_map())

        for i in range(current_keys_count):
            anim = key_anims[i]
            is_pressed = i in pressed

            target_val = 165.0 if is_pressed else 255.0
            target_scale = 0.94 if is_pressed else 1.0

            # Оптимізована інтерполяція колірних каналів
            c = anim['color']
            c[0] += (target_val - c[0]) * 0.25
            c[1] += (target_val - c[1]) * 0.25
            c[2] += (target_val - c[2]) * 0.25

            anim['scale'] += (target_scale - anim['scale']) * 0.25

            if anim['pulse'] > 0:
                anim['pulse'] = max(0.0, anim['pulse'] - 0.05)

    # Отрисовка
    screen.blit(BACKGROUND_IMG, (0, 0))

    if current_screen == "settings":
        if settings_menu:
            settings_menu.draw(screen)
    elif current_screen == "autoplay_menu":
        if autoplay_menu:
            autoplay_menu.draw(screen)
    else:
        if LOGO_IMG:
            screen.blit(LOGO_IMG, (LOGO_X, 25))

        draw_keys(screen, key_rects, key_anims)
        settings_btn.draw(screen)
        autoplay_btn.draw(screen)

        if midi_manager.is_playing:
            stop_btn.draw(screen)

    display.update()

quit()
