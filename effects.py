import pygame
from pygame import draw, Rect, Surface

# Кеші для повторного використання створених поверхонь з прозорістю
_GLASS_CACHE = {}
_SHADOW_CACHE = {}


def draw_glass_rect(screen, rect, base_color, alpha, border_color, border_alpha, radius=12, border_width=2):
    w, h = int(rect.width), int(rect.height)
    key = (w, h, tuple(base_color), alpha, tuple(border_color), border_alpha, radius, border_width)

    surf = _GLASS_CACHE.get(key)
    if surf is None:
        surf = Surface((w, h), pygame.SRCALPHA)
        draw.rect(surf, (*base_color, alpha), (0, 0, w, h), border_radius=radius)
        draw.rect(surf, (*border_color, border_alpha), (0, 0, w, h), border_width, border_radius=radius)
        _GLASS_CACHE[key] = surf

    screen.blit(surf, rect.topleft)


def draw_key_effect(screen, rect, color, offset, pulse_timer=0.0, scale=1.0):
    if scale != 1.0:
        new_w = int(rect.width * scale)
        new_h = int(rect.height * scale)
        new_x = rect.x + (rect.width - new_w) // 2
        new_y = rect.y + (rect.height - new_h) // 2
        draw_rect = Rect(new_x, new_y, new_w, new_h)
    else:
        draw_rect = rect

    # Оптимізоване відтворення тіні
    shadow_key = (draw_rect.width, draw_rect.height)
    shadow_surf = _SHADOW_CACHE.get(shadow_key)
    if shadow_surf is None:
        shadow_surf = Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        draw.rect(shadow_surf, (0, 0, 0, 35), (0, 0, draw_rect.width, draw_rect.height), border_radius=14)
        _SHADOW_CACHE[shadow_key] = shadow_surf

    screen.blit(shadow_surf, (draw_rect.x, draw_rect.y + 4))

    # Скляне тіло та рамка
    draw_glass_rect(screen, draw_rect, color, 145, (255, 255, 255), 210, radius=14, border_width=2)
    draw_glass_rect(screen, draw_rect, (0, 0, 0), 0, (0, 0, 0), 50, radius=14, border_width=1)

    # Ефект імпульсу (Pulse)
    if pulse_timer > 0:
        max_padding = int((1.5 - pulse_timer) * 25)
        glow_alpha = int(pulse_timer * 170)

        if glow_alpha > 0 and max_padding > 0:
            pw = draw_rect.width + max_padding * 2
            ph = draw_rect.height + max_padding * 2
            pulse_surf = Surface((pw, ph), pygame.SRCALPHA)
            draw.rect(pulse_surf, (255, 255, 255, glow_alpha), (0, 0, pw, ph), 2, border_radius=14 + max_padding)
            screen.blit(pulse_surf, (draw_rect.x - max_padding, draw_rect.y - max_padding))


def draw_button_flash(screen, rect, flash_timer):
    if flash_timer > 0:
        max_padding = int(flash_timer * 10)
        alpha = int(flash_timer * 25)
        for padding in range(1, max_padding):
            glow_rect = rect.inflate(padding * 2, padding * 2)
            draw.rect(screen, (255, 255, 255, alpha), glow_rect, 1, border_radius=10 + padding)
