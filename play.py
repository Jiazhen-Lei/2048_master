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

clock = pygame.time.Clock()  # 系统时间
board = Board(SIZE)  # 实例化board对象，传递参数size = 4

def btnBase():
    print("Start Base 2048")
    tip = 0
    while not board.over():
        clock.tick(60)
        GameState, tip = base.start_base_2048(board, buttonGroup, extip = tip)
        showAll(board, button = buttonGroup, operation = tip)
        if GameState:
            break
    if not GameState:
        print("游戏结束")
        pygame.time.delay(2000)
        pygame.quit()
        
def btnTip():
    tip = tip2048.tip_2048(board)
    return tip

def btnAI():
    print("Start AI 2048")
    while not board.over():
        clock.tick(60)
        GameState = AI2048.AI_2048(board, buttonGroup, 1000) #第二个参数调整AI快慢
        showAll(board, button = buttonGroup)
        if GameState:
            break
    print("游戏结束")
    # TODO 增加结束界面
    if not GameState:
        pygame.time.delay(2000)
        pygame.quit()
        
def btnNew():
    print("Please choose your new mode")
    board.__init__(SIZE)
    showAll(board, button = buttonGroup)
    return True

buttonBase = Button((10,90,70,40), buttonColorMap[0], btnBase, text="Base", **BUTTON_STYLE)
buttonTip = Button((100,90,70,40),  buttonColorMap[0], btnTip, text="Tip", **BUTTON_STYLE)
buttonAI = Button((190,90,70,40),  buttonColorMap[0], btnAI, text="AI", **BUTTON_STYLE)
buttonNew = Button((280,90,70,40),  buttonColorMap[0], btnNew, text="New", **BUTTON_STYLE)
buttonGroup = [buttonBase,buttonTip,buttonAI,buttonNew]

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
            
if __name__ == '__main__':
    pygame.init()
    play()
