import pygame
from pygame.locals import *
import time
from show.show import *
from board.board import *

# 基础2048
def start_base_2048(board: Board, button):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()  # 直接退出
        # 接收玩家操作
        elif event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:  # 上
                board.move_up()
                if(board.changed):
                    board.add()  # 添加一个新数
            elif event.key == K_s or event.key == K_DOWN:  # 下
                board.move_down()
                if(board.changed):
                    board.add()  # 添加一个新数
            elif event.key == K_a or event.key == K_LEFT:  # 左
                board.move_left()
                if(board.changed):
                    board.add()  # 添加一个新数
            elif event.key == K_d or event.key == K_RIGHT:  # 右
                board.move_right()
                if(board.changed):
                    board.add()  # 添加一个新数

        button[0].check_event(event)
        button[1].check_event(event)
        button[2].check_event(event)
        GameState = button[3].check_event(event)

        return GameState
