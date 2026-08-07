import os
import wave
import struct
import math
import random
import pygame
from settings import KEYS

BASE_SOUNDS_DIR = os.path.join("assets", "sounds")
GEN_SOUNDS_DIR = os.path.join("assets", "data", "sounds")

sounds = {}
generated_sounds = {}
use_random_sounds = False


def _ensure_mixer_initialized():
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.set_num_channels(64)


def init_base_sounds(volume=0.7):
    global sounds
    _ensure_mixer_initialized()
    sounds.clear()

    for key_name, file_name in KEYS.items():
        path = os.path.join(BASE_SOUNDS_DIR, file_name)
        if os.path.exists(path):
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(volume)
                sounds[key_name] = snd
            except Exception as e:
                print(f"Помилка завантаження базового звуку {path}: {e}")
                sounds[key_name] = None
        else:
            sounds[key_name] = None


def generate_wav_file(filepath, duration=0.6, sample_rate=44100):
    freq = random.uniform(180, 950)
    wave_type = random.choice(['sine', 'square', 'sawtooth', 'triangle'])

    num_samples = int(sample_rate * duration)
    max_amplitude = 15000
    fade_samples = int(0.04 * sample_rate)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    frames = bytearray()
    two_pi_freq = 2 * math.pi * freq

    for i in range(num_samples):
        t = i / sample_rate
        phase = (t * freq) % 1.0

        if wave_type == 'sine':
            val = math.sin(two_pi_freq * t)
        elif wave_type == 'square':
            val = 1.0 if phase < 0.5 else -1.0
        elif wave_type == 'sawtooth':
            val = 2.0 * phase - 1.0
        else:
            val = 4.0 * abs(phase - 0.5) - 1.0

        if i < fade_samples:
            envelope = i / fade_samples
        elif i > num_samples - fade_samples:
            envelope = (num_samples - i) / fade_samples
        else:
            envelope = 1.0

        sample_val = max(-32768, min(32767, int(val * max_amplitude * envelope)))
        frames.extend(struct.pack('<h', sample_val))

    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(frames)


def enable_random_sounds(current_volume=0.7):
    global generated_sounds, use_random_sounds
    _ensure_mixer_initialized()

    os.makedirs(GEN_SOUNDS_DIR, exist_ok=True)
    generated_sounds.clear()

    for idx, key_name in enumerate(KEYS.keys()):
        filename = f"gen_sound_{idx + 1}.wav"
        filepath = os.path.join(GEN_SOUNDS_DIR, filename)

        duration = random.uniform(0.4, 0.9)
        generate_wav_file(filepath, duration=duration)

        try:
            snd = pygame.mixer.Sound(filepath)
            snd.set_volume(current_volume)
            generated_sounds[key_name] = snd
        except Exception as e:
            print(f"Помилка створення звуку {filepath}: {e}")
            generated_sounds[key_name] = None

    use_random_sounds = True


def disable_random_sounds():
    global use_random_sounds
    use_random_sounds = False


def is_random_active():
    return use_random_sounds


def play_sound(key_name):
    target_map = generated_sounds if use_random_sounds else sounds
    snd = target_map.get(key_name)
    if snd:
        snd.play()


def get_active_sounds_map():
    return generated_sounds if use_random_sounds else sounds


def update_all_volumes(volume):
    for snd in sounds.values():
        if snd:
            snd.set_volume(volume)
    for snd in generated_sounds.values():
        if snd:
            snd.set_volume(volume)
