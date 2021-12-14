from board import *
import math
from pygame.locals import *
import pygame
import game.base2048 as base
import game.nAI2048 as AI2048
import game.ntip2048 as tip2048
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
                    if 20 < mouse_x < 90 and 90 < mouse_y < 130:
                        print("Start Base 2048")
                        while not board.over():
                            clock.tick(60)
                            base.start_base_2048(board, clock)
                            showAll(board)
                        print("游戏结束")
                        # TODO 增加结束界面
                        pygame.quit()
                        pygame.time.delay(2000)
                        break
                    elif 110 < mouse_x < 150 and 90 < mouse_y < 130:
                        print("Start Tip 2048")
                        tip = 0 # 初始化为空
                        while not board.over():
                            clock.tick(60)
                            tip = tip2048.tip_2048(board,tip)
                            showAll(board, tip)
                        print("游戏结束")
                        # TODO 增加结束界面
                        pygame.quit()
                        pygame.time.delay(2000)
                        break

                    elif 180 < mouse_x < 230 and 90 < mouse_y < 130:
                        print("Start AI 2048")
                        while not board.over():
                            clock.tick(60)
                            AI2048.AI_2048(board, 1000) #第二个参数调整AI快慢
                            showAll(board)
                        print("游戏结束")
                        # TODO 增加结束界面
                        pygame.quit()
                        pygame.time.delay(2000)
                        break


                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Please choose your new mode")
                    else:
                        continue


if __name__ == '__main__':
    play()
