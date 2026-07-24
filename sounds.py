import pygame
import os
from settings import KEYS

# ==============================================================================
# ======================== ІНІЦІАЛІЗАЦІЯ ТА ЗАВАНТАЖЕННЯ ЗВУКІВ =================
# ==============================================================================
pygame.mixer.init()

sounds = {}
for k, filename in KEYS.items():
    path = os.path.join("assets", "sounds", filename)
    try:
        sounds[k] = pygame.mixer.Sound(path)
    except pygame.error:
        # Змінено на None, якщо аудіофайл відсутній на диску
        sounds[k] = None