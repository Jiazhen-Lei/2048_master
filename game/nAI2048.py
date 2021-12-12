import game.val as val
from board import *

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
    '''
    num=0
    sum_val=0
    for i in range(size_x):
        for j in range(size_y):
            for k in range(1,3):
                if new[i][j]>0:
                    continue
                new[i][j]=k*2
                now_val = val.evaluation(new)
                if now_val<worst:
                    worst,ansx,ansy,ansk = now_val,i,j,k*2
                sum_val+=now_val
                num+=1
                new[i][j] = 0
    worst=sum_val/num
    '''

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


def AI_2048(board):
    now = board
    operation, best_val, can_move = dfs(now, 0, search_step)
    print('operation=', operation, 'best_val=', best_val)
    print(can_move)
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
