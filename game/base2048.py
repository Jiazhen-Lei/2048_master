import pygame
from pygame.locals import *
import time 

# 基础2048
def start_base_2048(board,clock):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # 直接退出
            #sys.exit()
    #接收玩家操作
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_w] or pressed_keys[K_UP]: # 上
        board.move_up()
        time.sleep(0.2)
    elif pressed_keys[K_s] or pressed_keys[K_DOWN]: # 下
        board.move_down()
        time.sleep(0.2)
    elif pressed_keys[K_a] or pressed_keys[K_LEFT]: # 左
        board.move_left()
        time.sleep(0.2)
    elif pressed_keys[K_d] or pressed_keys[K_RIGHT]: # 右
        board.move_right()
        time.sleep(0.2)
