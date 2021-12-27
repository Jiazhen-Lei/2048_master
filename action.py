import game.base2048 as base
import game.AI2048 as AI2048
import game.tip2048 as tip2048
from button import Button
from sound.sound import *
from show.show import *
from show.showConfig import *

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
        tip = 5
        failSound()
        showAll(board, button = buttonGroup, operation = tip)
        while not GameState: 
            GameState, tip = base.start_base_2048(board, buttonGroup, extip = tip)
            showAll(board, button = buttonGroup, operation = tip)
            if GameState:
                break
def btnTip():
    tip = tip2048.tip_2048(board)
    return tip

def btnAI():
    print("Start AI 2048")
    while not board.over():
        clock.tick(60)
        GameState = AI2048.AI_2048(board, buttonGroup, 10) #第二个参数调整AI快慢
        showAll(board, button = buttonGroup)
        if GameState:
            break
    # TODO 增加结束界面
    if not GameState:
        print("游戏结束")
        failSound()
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
