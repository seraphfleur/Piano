from pygame import Rect
from effects import draw_key_effect

# ==============================================================================
# ======================== ЛОГІКА ТА ВІДМАЛЬОВКА КЛАВІШ =========================
# ==============================================================================
def draw_keys(screen, key_rects, key_anims):
    for i, rect in enumerate(key_rects):
        anim = key_anims[i]
        # Передаємо колір, зсув, таймер пульсації та коефіцієнт зменшення
        draw_key_effect(screen, rect, anim['color'], anim['offset'], anim.get('pulse', 0.0), anim.get('scale', 1.0))

def create_key_rects(num_keys, start_x=50, start_y=120, key_width=100, key_height=240):
    rects = []
    for i in range(num_keys):
        x = start_x + i * key_width
        rects.append(Rect(x, start_y, key_width, key_height))
    return rects
