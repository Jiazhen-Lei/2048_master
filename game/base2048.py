import pygame
from pygame.locals import *
import time
from show.show import *
from board.board import *

# 基础2048


def start_base_2048(board: Board, clock):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()  # 直接退出
        # 接收玩家操作
        elif event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:  # 上
                board.move_up()
                if(board.changed):
                    board.add()  # 添加一个新数
                # time.sleep(0.2)
            elif event.key == K_s or event.key == K_DOWN:  # 下
                board.move_down()
                if(board.changed):
                    board.add()  # 添加一个新数
                # time.sleep(0.2)
            elif event.key == K_a or event.key == K_LEFT:  # 左
                board.move_left()
                if(board.changed):
                    board.add()  # 添加一个新数
                # time.sleep(0.2)
            elif event.key == K_d or event.key == K_RIGHT:  # 右
                board.move_right()
                if(board.changed):
                    board.add()  # 添加一个新数
                # time.sleep(0.2)
            return False

        elif MOUSEBUTTONDOWN == event.type:
            pressed_array = pygame.mouse.get_pressed()
            if pressed_array[0] == 1: # 左键被按下
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]  # x坐标
                mouse_y = pos[1]  # y坐标
                if 280 < mouse_x < 350 and 90 < mouse_y < 130:
                    showBotton(4)
                    pygame.display.update()
                    return False

        elif MOUSEBUTTONUP == event.type:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]  # x坐标
            mouse_y = pos[1]  # y坐标
            if 280 < mouse_x < 350 and 90 < mouse_y < 130:
                print("Please choose your new mode")
                board.__init__(SIZE)
                showAll(board)
                return True
