from board import *
import math
from pygame.locals import *
import pygame
import game.base2048 as base
import game.nAI2048 as AI2048
from pygame import display
import sys
from show import *
import time
import random


# import game.tip2048 as tip
# import game.ai2048 as ai


def play():
    clock = pygame.time.Clock()  # 系统时间
    board = Board(SIZE)  # 实例化board对象，传递参数size = 4
    board.debug = True
    showAll(board)  # 显示
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
            if MOUSEBUTTONDOWN == event.type:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0] == 1:
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0]  # x坐标
                    mouse_y = pos[1]  # y坐标
                    if 40 < mouse_x < 90 and 90 < mouse_y < 130:
                        print("Start Base 2048")
                        while not board.over():
                            clock.tick(60)
                            base.start_base_2048(board, clock)
                            # AI2048.AI_2048(board)
                            showAll(board)
                        print("游戏结束")
                        # TODO 增加结束界面
                        pygame.quit()
                        pygame.time.delay(2000)
                        break
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Start Tip 2048")
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Start AI 2048")
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Please choose your new mode")
                    else:
                        continue


if __name__ == '__main__':
    play()
