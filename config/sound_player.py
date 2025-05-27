import pygame
import time

pygame.mixer.init()

def play_sound(path, duration):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        time.sleep(duration)
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"[ERROR] Playing sound: {e}")

