import game.val as val
from pygame.locals import *
import pygame
from board.board import *

search_step = 3
size_x = size_y = SIZE = 4


def worst_val(map):
    new = map
    ansx = ansy = ansk = 0
    worst = 10000

    for i in range(size_x):
        for j in range(size_y):
            for k in range(1, 3):
                if new[i][j] > 0:
                    continue
                new[i][j] = k*2
                now_val = val.evaluation(new)
                if now_val < worst:
                    worst, ansx, ansy, ansk = now_val, i, j, k*2
                new[i][j] = 0
    return worst, ansx, ansy, ansk


def dfs(board, now_step, limit_step):
    can_move = [True for i in range(4)]
    move = [board for i in range(4)]
    new = Board(SIZE, board.map)
    move[0], can_move[0] = new.move_up()
    new = Board(SIZE, board.map)
    move[1], can_move[1] = new.move_down()
    new = Board(SIZE, board.map)
    move[2], can_move[2] = new.move_left()
    new = Board(SIZE, board.map)
    move[3], can_move[3] = new.move_right()
    best_move = -1
    best_val = -1
    if now_step == limit_step:
        for i in range(4):
            if not can_move[i]:
                continue
            val_now, x, y, k = worst_val(move[i].numMap())
            if val_now > best_val:
                best_move = i
                best_val = val_now
    else:
        for i in range(4):
            if not can_move[i]:
                continue
            val_now, x, y, k = worst_val(move[i].numMap())
            move[i].add_xy(x, y, k)
            now_move, val_now, blank_move = dfs(
                move[i], now_step+1, limit_step)
            val_now = max(0, val_now)
            if val_now > best_val:
                best_move = i
                best_val = val_now
    # print(now_step,best_move,best_val)
    # print(board.map)
    return best_move, best_val, can_move


lastTime = pygame.time.get_ticks()


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
            