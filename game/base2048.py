import pygame
from pygame.locals import *
from show.show import *
from board.board import *
from sound.sound import *

# 基础2048
def start_base_2048(board: Board, button, extip):
    """
    Base2048模式
    功能:
        根据pygame事件，进行游戏的上下左右移动和按键检测
    参数:
        board:实例board界面
        button:按键对象列表
        extip:上一次tip索引
    返回值:
        GameState:默认为False，当判断New按键操作时为True重置board
        tip:本次tip索引
    """
    GameState = False
    tip = extip
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()  # 直接退出
        # 接收玩家操作
        elif event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:  # 上
                board.move_up()
                slideSound()
                if(board.changed):
                    board.add()  # 添加一个新数
            elif event.key == K_s or event.key == K_DOWN:  # 下
                board.move_down()
                slideSound()
                if(board.changed):
                    board.add()  # 添加一个新数
            elif event.key == K_a or event.key == K_LEFT:  # 左
                board.move_left()
                slideSound()
                if(board.changed):
                    board.add()  # 添加一个新数
            elif event.key == K_d or event.key == K_RIGHT:  # 右
                board.move_right()
                slideSound()
                if(board.changed):
                    board.add()  # 添加一个新数

        button[0].check_event(event)
        tip = button[1].check_event(event,tip = tip)
        button[2].check_event(event)
        GameState = button[3].check_event(event)

    return GameState, tip
