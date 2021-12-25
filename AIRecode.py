import numpy as np
from numpy.lib.function_base import average
from board import *
import game.nAI2048 as AI2048
import os


# import game.tip2048 as tip
# import game.ai2048 as ai


def play(t):
    scores=[]
    nums=[]
    avgScore = 0
    bestScore = 0
    maxNum = 0
    avgNum = 0
    board = Board(4)  # 实例化board对象，传递参数size = 4
    # board.debug = True
    for i in range(t):
        board = Board(4)
        while not board.over():
            # os.system('cls')
            AI2048.AI_2048(board, 1, noGame=True)  # 第二个参数调整AI快慢
        scores.append(board.score)
        nums.append(np.max(board.numMap()))
        print('the',i,'run')

        avgScore = average(scores) 
        bestScore = max(scores)
        avgNum = average(nums)
        maxNum = max(nums)
        print('maxNum:', maxNum, 'avgNum:', avgNum)
        print('bestScore:', bestScore, 'avgScore:', avgScore)


if __name__ == '__main__':
    os.system("cls")
    play(10)
