from numpy.core.fromnumeric import size
from pygame.locals import *
import pygame
from show.show import *
from action import *

def play():
    # board.debug = True
    showAll(board, button = buttonGroup)  # 显示
    while  True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
            clock.tick(60)
            buttonBase.check_event(event)
            buttonTip.check_event(event)
            buttonAI.check_event(event)
            buttonNew.check_event(event)
            showAll(board, button = buttonGroup)

if __name__ == '__main__':
    pygame.init() 
    play()
