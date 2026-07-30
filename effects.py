import pygame
from pygame import draw, Rect, Surface


# ==============================================================================
# ======================== УНІВЕРСАЛЬНИЙ РЕНДЕР СКЛА ===========================
# ==============================================================================
def draw_glass_rect(screen, rect, base_color, alpha, border_color, border_alpha, radius=12, border_width=2):
    surf = Surface((rect.width, rect.height), pygame.SRCALPHA)
    draw.rect(surf, (*base_color, alpha), (0, 0, rect.width, rect.height), border_radius=radius)
    draw.rect(surf, (*border_color, border_alpha), (0, 0, rect.width, rect.height), border_width, border_radius=radius)
    screen.blit(surf, rect.topleft)


# ==============================================================================
# ========================= ВІЗУАЛЬНІ ЕФЕКТИ КЛАВІШ ============================
# ==============================================================================
def draw_key_effect(screen, rect, color, offset, pulse_timer=0.0, scale=1.0):
    # Розрахунок зменшеного розміру клавіші відносно її геометричного центру
    if scale != 1.0:
        new_w = int(rect.width * scale)
        new_h = int(rect.height * scale)
        new_x = rect.x + (rect.width - new_w) // 2
        new_y = rect.y + (rect.height - new_h) // 2
        draw_rect = Rect(new_x, new_y, new_w, new_h)
    else:
        draw_rect = rect.copy()

    # Тінь під клавішею (адаптується під новий розмір)
    shadow_surf = Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
    draw.rect(shadow_surf, (0, 0, 0, 35), (0, 0, draw_rect.width, draw_rect.height), border_radius=14)
    screen.blit(shadow_surf, (draw_rect.x, draw_rect.y + 4))

    # Малюємо основне скляне тіло клавіші (колір містить затемнення)
    draw_glass_rect(screen, draw_rect, color, 145, (255, 255, 255), 210, radius=14, border_width=2)

    # Додаткова тонка темна рамка
    draw_glass_rect(screen, draw_rect, (0, 0, 0), 0, (0, 0, 0), 50, radius=14, border_width=1)

    # ВІЗУАЛЬНИЙ ЕФЕКТ: БІЛИЙ PULSE (спрацьовує поверх зменшеної клавіші)
    if pulse_timer > 0:
        max_padding = int((1.5 - pulse_timer) * 25)
        glow_alpha = int(pulse_timer * 170)

        if glow_alpha > 0 and max_padding > 0:
            pulse_surf = Surface((draw_rect.width + max_padding * 2, draw_rect.height + max_padding * 2),
                                 pygame.SRCALPHA)
            draw.rect(pulse_surf, (255, 255, 255, glow_alpha),
                      (0, 0, pulse_surf.get_width(), pulse_surf.get_height()),
                      2, border_radius=14 + max_padding)
            screen.blit(pulse_surf, (draw_rect.x - max_padding, draw_rect.y - max_padding))


# ==============================================================================
# ======================== ЕФЕКТИ ДЛЯ КНОПОК МЕНЮ ==============================
# ==============================================================================
def draw_button_flash(screen, rect, flash_timer):
    if flash_timer > 0:
        for padding in range(1, int(flash_timer * 10)):
            glow_rect = rect.inflate(padding * 2, padding * 2)
            draw.rect(screen, (255, 255, 255, int(flash_timer * 25)), glow_rect, 1, border_radius=10 + padding)
