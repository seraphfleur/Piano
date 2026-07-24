from pygame import draw, Rect
from settings import BLACK

# ==============================================================================
# ========================= ВІЗУАЛЬНІ ЕФЕКТИ КЛАВІШ ============================
# ==============================================================================
def draw_key_effect(screen, rect, color, offset):
    # Малюємо темну тінь, яка створює 3D-ефект
    shadow_rect = rect.copy()
    draw.rect(screen, (80, 80, 80), shadow_rect, border_radius=8)
    
    # Зсуваємо лицьову сторону клавіші вниз на величину offset
    face_rect = rect.move(0, offset)
    
    # Малюємо клавішу з поточним плавним кольором
    draw.rect(screen, color, face_rect, border_radius=8)
    draw.rect(screen, BLACK, face_rect, 2, border_radius=8)
    
    # Ефект спалаху: якщо клавіша натиснута глибоко, додаємо білий відблиск вгорі
    if offset > 4:
        flash_rect = Rect(face_rect.x + 6, face_rect.y + 6, face_rect.width - 12, 6)
        draw.rect(screen, (255, 255, 255), flash_rect, border_radius=3)

# ==============================================================================
# ======================== ЕФЕКТИ ДЛЯ КНОПОК МЕНЮ ==============================
# ==============================================================================
def draw_button_flash(screen, rect, flash_timer):
    # Коротке підсвічування навколо кнопки при кліку
    if flash_timer > 0:
        glow_color = (255, 215, 0) # Золотий колір спалаху
        # Створюємо ефект хвилі, що розширюється
        for padding in range(1, int(flash_timer * 12)):
            glow_rect = rect.inflate(padding * 2, padding * 2)
            draw.rect(screen, glow_color, glow_rect, 1, border_radius=5 + padding)
