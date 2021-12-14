import game.val as val
from pygame.locals import *
import pygame
from board.board import *
from game.nAI2048 import *

def get_tip(board, gap=50):
    global lastTime
    if pygame.time.get_ticks() - lastTime > gap:
        lastTime = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # 直接退出

        now = board
        operation, best_val, can_move = dfs(now, 0, search_step)
        print('operation=', operation, 'best_val=', best_val)
        print(can_move)
        return operation+1

def tip_2048(board: Board, tip):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()  # 直接退出
            # sys.exit()
        # 接收玩家操作
        elif event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:  # 上
                board.move_up()
                if(board.changed):
                    board.add()  # 添加一个新数
                    tip = get_tip(board, 50)
                    return tip
                # time.sleep(0.2)
            elif event.key == K_s or event.key == K_DOWN:  # 下
                board.move_down()
                if(board.changed):
                    board.add()  # 添加一个新数
                    tip = get_tip(board, 50)
                    return tip
                # time.sleep(0.2)
            elif event.key == K_a or event.key == K_LEFT:  # 左
                board.move_left()
                if(board.changed):
                    board.add()  # 添加一个新数
                    tip = get_tip(board, 50)
                    return tip
                # time.sleep(0.2)
            elif event.key == K_d or event.key == K_RIGHT:  # 右
                board.move_right()
                if(board.changed):
                    board.add()  # 添加一个新数
                    tip = get_tip(board, 50)
                    return tip
                # time.sleep(0.2)

    return tip
            