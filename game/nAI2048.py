import game.val as val
import pygame
from board import *
from pygame.locals import *
from show.show import *

search_step = 3
size_x = size_y = SIZE = 4


def worst_val(map):
    new = map.numMap()
    ansx = ansy = ansk = 0
    worst = [1000000]

    for i in range(size_x):
        for j in range(size_y):
            for k in range(1, 3):
                if new[i][j] > 0:
                    continue
                new[i][j] = k*2
                now_val = val.evaluation(new, map.score)
                if sum(now_val) < sum(worst):
                    worst, ansx, ansy, ansk = now_val, i, j, k*2
                new[i][j] = 0

    return worst, ansx, ansy, ansk


def dfs(board: Board, now_step, limit_step):
    can_move = [True for i in range(4)]
    move = [board for i in range(4)]
    if now_step == 0:
        new = Board(SIZE, board.map)
        move[0], can_move[0], _ = new.move_up()
        new = Board(SIZE, board.map)
        move[1], can_move[1], _ = new.move_down()
        new = Board(SIZE, board.map)
        move[2], can_move[2], _ = new.move_left()
        new = Board(SIZE, board.map)
        move[3], can_move[3], _ = new.move_right()
    else:
        new = Board(SIZE, board.map, board.score)
        move[0], can_move[0], _ = new.move_up()
        new = Board(SIZE, board.map, board.score)
        move[1], can_move[1], _ = new.move_down()
        new = Board(SIZE, board.map, board.score)
        move[2], can_move[2], _ = new.move_left()
        new = Board(SIZE, board.map, board.score)
        move[3], can_move[3], _ = new.move_right()
    best_move = -1
    best_val = [-1]
    if now_step == limit_step:
        for i in range(4):
            if not can_move[i]:
                continue
            val_now, x, y, k = worst_val(move[i])
            if sum(val_now) > sum(best_val):
                best_move = i
                best_val = val_now
    else:
        for i in range(4):
            if not can_move[i]:
                continue
            val_now, x, y, k = worst_val(move[i])
            move[i].add_xy(x, y, k)
            now_move, val_now, blank_move = dfs(
                move[i], now_step+1, limit_step)
            # val_now = max(0, val_now)
            val_now = [0] if sum(val_now) <= 0 else val_now
            if sum(val_now) > sum(best_val):
                best_move = i
                best_val = val_now
    # print(now_step,best_move,best_val)
    # print(board.map)
    return best_move, best_val, can_move


lastTime = pygame.time.get_ticks()


def AI_2048(board: Board, gap=50):
    global lastTime
    if pygame.time.get_ticks() - lastTime > gap:
        lastTime = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # 直接退出
            elif MOUSEBUTTONDOWN == event.type:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0] == 1:  # 左键被按下
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

        now = board
        operation, best_val, can_move = dfs(now, 0, search_step)
        print('operation=', operation, 'best_val=', best_val)
        print(can_move)
        board.mapPrint()
        if operation == 0:
            board.move_up()
            if(board.changed):
                board.add()  # 添加一个新数
        elif operation == 1:
            board.move_down()
            if(board.changed):
                board.add()  # 添加一个新数
        elif operation == 2:
            board.move_left()
            if(board.changed):
                board.add()  # 添加一个新数
        elif operation == 3:
            board.move_right()
            if(board.changed):
                board.add()  # 添加一个新数
            # time.sleep(0.1)
        return False  # 不需要重启
