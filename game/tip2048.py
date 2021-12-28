from pygame.locals import *
from board.board import *
from game.AI2048 import *

def tip_2048(board, gap=50):
    """
    tip2048
    功能:
        调用一次AI算法，计算一次下一步
    参数:
        board:实例board界面
        gap:AI算法速度，默认50
    返回值:
        operation+1:tip索引,对应tip文字地图中显示字符串
    """
    global lastTime
    if int(time.time()*1000) - lastTime > gap:
        lastTime = int(time.time()*1000)
        
        now = board
        operation = getBestMove(now)
        return operation+1