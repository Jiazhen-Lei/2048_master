import pygame

def failSound():
    """失败音效触发函数"""
    pygame.mixer.Sound("./sound/failed.wav").play()

def slideSound():
    """滑动音效触发函数"""
    pygame.mixer.Sound("./sound/slided.wav").play()