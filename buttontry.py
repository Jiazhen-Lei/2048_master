from numpy.core.fromnumeric import size
from board import *
from pygame.locals import *
import pygame
import game.base2048 as base
import game.nAI2048 as AI2048
import game.ntip2048 as tip2048
from show.show import *
from show.showConfig import *
from button import Button

def btnBase():
    print("base")

def btnTip():
    print("tip")

def btnAI():
    print("AI")

def btnNew():
    print("new")

def play():
    # board.debug = True
    showAll(board, button = buttonGroup)  # 显示
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
            clock.tick(60)
            buttonBase.check_event(event)
            buttonTip.check_event(event)
            buttonAI.check_event(event)
            buttonNew.check_event(event)
            showAll(board, button = buttonGroup)
            buttonBase.update(screen_display)
            pygame.display.update()  # 更新显示
            
if __name__ == '__main__':
    clock = pygame.time.Clock()  # 系统时间
    board = Board(SIZE)  # 实例化board对象，传递参数size = 4
    buttonBase = Button((10,90,70,40), buttonColorMap[0], btnBase, text="Base", **BUTTON_STYLE)
    buttonTip = Button((100,90,70,40),  buttonColorMap[0], btnTip, text="Tip", **BUTTON_STYLE)
    buttonAI = Button((190,90,70,40),  buttonColorMap[0], btnAI, text="AI", **BUTTON_STYLE)
    buttonNew = Button((280,90,70,40),  buttonColorMap[0], btnNew, text="New", **BUTTON_STYLE)
    buttonGroup = [buttonBase,buttonTip,buttonAI,buttonNew]

    play()
