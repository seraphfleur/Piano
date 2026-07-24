import pygame
from pygame import *
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, keys_list
from keys import create_key_rects, draw_keys
from sounds import sounds
from buttons import Button

# ==============================================================================
# ============================ СТАРТ ПРОЄКТУ ТА ВІКНО ===========================
# ==============================================================================
init()
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Piano Game")
running = True

# ==============================================================================
# =========================== ІНІЦІАЛІЗАЦІЯ ОБ'ЄКТІВ ===========================
# ==============================================================================
pressed = set()
key_rects = create_key_rects(7)
settings_btn = Button("Settings", 20, 20, 100, 40)

# ==============================================================================
# ============================ ГОЛОВНИЙ ЦИКЛ ГРИ ===============================
# ==============================================================================
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

        # ------------------------- МЕХАНІКА КЛАВІАТУРИ -------------------------
        if e.type == KEYDOWN:
            k = key.name(e.key)
            if k in sounds:
                if sounds[k]:
                    sounds[k].play()
                pressed.add(keys_list.index(k))

        if e.type == KEYUP:
            k = key.name(e.key)
            if k in keys_list:
                idx = keys_list.index(k)
                pressed.discard(idx)

        # --------------------------- МЕХАНІКА МИШІ -----------------------------
        if e.type == MOUSEBUTTONDOWN:
            if settings_btn.collidepoint(e.pos):
                print("Відкрито меню налаштувань (Settings)!")

            for i, r in enumerate(key_rects):
                if r.collidepoint(e.pos):
                    k = keys_list[i]
                    if sounds[k]:
                        sounds[k].play()
                    pressed.add(i)

        if e.type == MOUSEBUTTONUP:
            for i, r in enumerate(key_rects):
                if i in pressed and r.collidepoint(e.pos):
                    pressed.remove(i)

    # -------------------------- ОНОВЛЕННЯ ЕКРАНУ ---------------------------
    screen.fill(WHITE)
    draw_keys(screen, key_rects, pressed)
    settings_btn.draw(screen)
    display.update()

quit()