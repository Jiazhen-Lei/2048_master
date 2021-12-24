
import numpy as np
import sys
sys.path.append("..")
from board import Board
from game import val


def max_num(map):
    max_num = 0
    for i in range(4):
        for j in range(4):
            if max_num < map[i][j]:
                max_num = map[i][j]
    return max_num


noChangedNum = 0


def myStep(board: Board, a):
    global noChangedNum
    _, changed, score_r = board.move(a)  # 简单的把当前步骤得分作为奖励
    board.add()
    max_r = max_num(board.numMap())
    # r = sum(val.evaluation(board.numMap(), score_r))/100
    # r = score_r/100+np.log2(max_r)/10
    r = score_r/100
    # s_ = np.reshape(board.numMap(), [1, -1])[0]
    s_ = board.numMap()
    over = board.over()
    if not changed:
        noChangedNum += 1
        r = -1*noChangedNum
    else:
        noChangedNum = 0
    if noChangedNum >= 10:
        over = True
    if over:
        r = -10
    return s_, r, over, max_r
