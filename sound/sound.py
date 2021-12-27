import pygame

def failSound():
    pygame.mixer.Sound("./sound/failed.wav").play()

def slideSound():
    pygame.mixer.Sound("./sound/slided.wav").play()