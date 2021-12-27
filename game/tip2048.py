from pygame.locals import *
from board.board import *
from game.AI2048 import *

def tip_2048(board, gap=50):
    global lastTime
    if int(time.time()*1000) - lastTime > gap:
        lastTime = int(time.time()*1000)
        
        now = board
        operation = getBestMove(now)
        return operation+1