from numpy.core.fromnumeric import size
from board import *
from pygame.locals import *
import pygame
import game.base2048 as base
import game.nAI2048 as AI2048
import game.ntip2048 as tip2048
from show.show import *
from show.showConfig import *

def play():
    clock = pygame.time.Clock()  # 系统时间
    board = Board(SIZE)  # 实例化board对象，传递参数size = 4
    # board.debug = True
    showAll(board)  # 显示
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
            if MOUSEBUTTONDOWN == event.type:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0] == 1: # 左键被按下
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0]  # x坐标
                    mouse_y = pos[1]  # y坐标
                    if 10 < mouse_x < 80 and 90 < mouse_y < 130:
                        showBotton(1)
                        pygame.display.update()
                    elif 100 < mouse_x < 170 and 90 < mouse_y < 130:
                        showBotton(2)
                        pygame.display.update()
                    elif 190 < mouse_x < 260 and 90 < mouse_y < 130:
                        showBotton(3)
                        pygame.display.update()
                    elif 280 < mouse_x < 350 and 90 < mouse_y < 130:
                        showBotton(4)
                        pygame.display.update()


            if MOUSEBUTTONUP == event.type:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]  # x坐标
                mouse_y = pos[1]  # y坐标
                if 10 < mouse_x < 80 and 90 < mouse_y < 130:
                    print("Start Base 2048")
                    while not board.over():
                        clock.tick(60)
                        GameState = base.start_base_2048(board, clock)
                        showAll(board)
                        if GameState:
                            break
                    print("游戏结束")
                    # TODO 增加结束界面
                    if not GameState:
                        pygame.quit()
                        pygame.time.delay(2000)
                        break
                elif 100 < mouse_x < 170 and 90 < mouse_y < 130:
                    print("Start Tip 2048")
                    tip = 4 # 初始化为空
                    while not board.over():
                        clock.tick(60)
                        tip, GameState = tip2048.tip_2048(board,tip)
                        showAll(board, tip)
                        if GameState:
                            tip = 4
                            showAll(board, tip)
                            break
                    print("游戏结束")
                    # TODO 增加结束界面
                    if not GameState:
                        pygame.quit()
                        pygame.time.delay(2000)
                        break

                elif 190 < mouse_x < 260 and 90 < mouse_y < 130:
                    print("Start AI 2048")
                    while not board.over():
                        clock.tick(60)
                        GameState = AI2048.AI_2048(board, 1000) #第二个参数调整AI快慢
                        showAll(board)
                        if GameState:
                            break
                    print("游戏结束")
                    # TODO 增加结束界面
                    if not GameState:
                        pygame.quit()
                        pygame.time.delay(2000)
                        break
                elif 280 < mouse_x < 350 and 90 < mouse_y < 130:
                    print("Please choose your new mode")
                    board.__init__(SIZE)
                    showAll(board)
                else:
                    continue

if __name__ == '__main__':
    pygame.init()
    play()
