from pygame.locals import *
import pygame
from show.show import *
from action import *

def play():
    showAll(board, button = buttonGroup)  # 显示
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
            clock.tick(60)
            # 按键事件判断 #
            buttonBase.check_event(event)
            buttonTip.check_event(event)
            buttonAI.check_event(event)
            buttonNew.check_event(event)
            showAll(board, button = buttonGroup) # 显示

if __name__ == '__main__':
    pygame.display.set_caption("2048") # 设置窗口标题
    play() # 开始游戏
