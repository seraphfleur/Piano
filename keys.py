from pygame import Rect
from effects import draw_key_effect


def draw_keys(screen, key_rects, key_anims):
    for i, rect in enumerate(key_rects):
        anim = key_anims[i]
        draw_key_effect(screen, rect, anim['color'], anim['offset'], anim.get('pulse', 0.0), anim.get('scale', 1.0))


def create_key_rects(num_keys, start_x=50, key_width=100):
    rects = []
    keys_per_row = 7
    is_single_row = num_keys <= 7

    for i in range(num_keys):
        row = i // keys_per_row
        col = i % keys_per_row

        if is_single_row:
            start_y = 120
            key_height = 240
        else:
            start_y = 95 + row * 135
            key_height = 115

        x = start_x + col * key_width
        rects.append(Rect(x, start_y, key_width, key_height))

    return rects
