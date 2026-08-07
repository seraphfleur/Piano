import os

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

FONT_PATH = os.path.join("assets", "fonts", "copperplate_light.otf")

KEYS = {
    # ВЕРХНІЙ РЯД (Ряд 1)
    "q": "a6.mp3",
    "w": "b6.mp3",
    "e": "d6.mp3",
    "r": "f6.mp3",
    "t": "g6.mp3",
    "y": "e6.mp3",
    "u": "c6.mp3",

    # НИЖНІЙ РЯД (Ряд 2)
    "a": "a6.mp3",
    "s": "b6.mp3",
    "d": "d6.mp3",
    "f": "f6.mp3",
    "g": "g6.mp3",
    "h": "e6.mp3",
    "j": "c6.mp3"
}

keys_list = list(KEYS.keys())
