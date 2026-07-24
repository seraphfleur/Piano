import pygame
from pygame import *
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, keys_list, FPS
from keys import create_key_rects, draw_keys
from sounds import sounds
from buttons import Button

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
# Завантаження фону (якщо файлу немає — створюється заливка)
try:
    BACKGROUND_IMG = image.load('assets/images/background.png')
    BACKGROUND_IMG = transform.scale(BACKGROUND_IMG, (WINDOW_WIDTH, WINDOW_HEIGHT))
except error:
    BACKGROUND_IMG = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    BACKGROUND_IMG.fill((235, 235, 242))

# Завантаження логотипу гри (розміщується над клавішами по центру)
try:
    LOGO_IMG = image.load('assets/images/logo.png')
    LOGO_IMG = transform.scale(LOGO_IMG, (220, 60))
except error:
    LOGO_IMG = None

# ==============================================================================
# =========================== ІНІЦІАЛІЗАЦІЯ ОБ'ЄКТІВ ===========================
# ==============================================================================
pressed = set()
key_rects = create_key_rects(7)
settings_btn = Button("Settings", 20, 20, 100, 40)

# Налаштування початкових параметрів для плавних анімацій клавіш
key_anims = []
for _ in range(7):
    key_anims.append({
        'color': [220, 220, 220], # Поточний RGB колір клавіші
        'offset': 0.0             # Поточний зсув вниз у пікселях
    })

# ==============================================================================
# ============================ ГОЛОВНИЙ ЦИКЛ ГРИ ===============================
# ==============================================================================
while running:
    # Обмеження частоти кадрів та отримання позиції миші
    clock.tick(FPS)
    mouse_pos = mouse.get_pos()
    settings_btn.update(mouse_pos)

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
                settings_btn.flash_timer = 1.5 # Запускаємо спалах навколо кнопки
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

    # ----------------------- ОБЧИСЛЕННЯ ПЛАВНИХ АНІМАЦІЙ --------------------
    for i in range(7):
        is_pressed = i in pressed
        
        # Визначаємо фінальні цілі, до яких прагне колір та зсув клавіші
        target_color = [170, 220, 255] if is_pressed else [220, 220, 220]
        target_offset = 7.0 if is_pressed else 0.0
        
        # Плавний перехід кольору через математичне наближення кроками
        for c_idx in range(3):
            key_anims[i]['color'][c_idx] += (target_color[c_idx] - key_anims[i]['color'][c_idx]) * 0.2
            
        # Плавне натискання клавіші вниз та повернення вгору
        key_anims[i]['offset'] += (target_offset - key_anims[i]['offset']) * 0.25

    # -------------------------- ОНОВЛЕННЯ ЕКРАНУ ---------------------------
    # Малюємо фон
    screen.blit(BACKGROUND_IMG, (0, 0))
    
    # Малюємо логотип гри по центру над клавішами, якщо він завантажився
    if LOGO_IMG:
        logo_x = (WINDOW_WIDTH - LOGO_IMG.get_width()) // 2
        screen.blit(LOGO_IMG, (logo_x, 25))
    
    # Відмальовуємо інтерфейс кнопок та клавіші з анімацією
    draw_keys(screen, key_rects, key_anims)
    settings_btn.draw(screen)
    
    display.update()

quit()
