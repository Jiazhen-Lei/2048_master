import game.base2048 as base
import game.AI2048 as AI2048
import game.tip2048 as tip2048
from button import Button
from sound.sound import *
from show.show import *
from show.showConfig import *

# 系统时间 #
clock = pygame.time.Clock()
# 实例化board对象，传递参数size = 4
board = Board(SIZE) 

def btnBase():
    """
    Base按键回调函数
    
    实现Base按键按下后的具体事件，即开启Base2048模式
    """
    print("Start Base 2048")
    tip = 0
    while not board.over():
        clock.tick(60) # fps
        GameState, tip = base.start_base_2048(board, buttonGroup, extip = tip) # 调用Base模式，第三个参数为当前tip索引
        showAll(board, button = buttonGroup, operation = tip) # 显示
        if GameState:
            break
    if not GameState:
        tip = 5 # Game over
        failSound() 
        showAll(board, button = buttonGroup, operation = tip) # 显示
        while not GameState: 
            GameState, tip = base.start_base_2048(board, buttonGroup, extip = tip) # 等待New
            showAll(board, button = buttonGroup, operation = tip) # 显示
            if GameState:
                break

def btnTip():
    """
    Tip按键回调函数
    
    实现Tip按键按下后的具体事件，即在base模式下进行tip提醒
    只可在Base模式下有效果

    返回值: 
        AI算法后的执行操作索引
    """
    tip = tip2048.tip_2048(board) # 调用tip
    return tip

def btnAI():
    """
    AI按键回调函数
    
    实现AI按键按下后的具体事件，即开启AI2048模式
    """
    print("Start AI 2048")
    while not board.over():
        clock.tick(60) # fps
        GameState = AI2048.AI_2048(board, buttonGroup, 10) #第二个参数调整AI快慢，10较快动画较卡顿，1000较慢，动画较流畅
        showAll(board, button = buttonGroup) # 显示
        if GameState:
            break
    if not GameState:
        failSound()
        pygame.time.delay(2000)
        pygame.quit()
        
def btnNew():
    """
    New按键回调函数
    
    实现New按键按下后的具体事件，即中断当前模式，回归初始化界面，board重置，需要重新选择模式

    返回值:
        为bool变量True，即重置，但不结束游戏
    """
    print("Please choose your new mode")
    board.__init__(SIZE) # board初始化
    showAll(board, button = buttonGroup) # 显示
    return True

# 实例化按键 传递参数按键位置大小，颜色，回调函数，显示文字，其他配置 #
buttonBase = Button((10,90,70,40), buttonColorMap[0], btnBase, text="Base", **BUTTON_STYLE)
buttonTip = Button((100,90,70,40),  buttonColorMap[0], btnTip, text="Tip", **BUTTON_STYLE)
buttonAI = Button((190,90,70,40),  buttonColorMap[0], btnAI, text="AI", **BUTTON_STYLE)
buttonNew = Button((280,90,70,40),  buttonColorMap[0], btnNew, text="New", **BUTTON_STYLE)
buttonGroup = [buttonBase,buttonTip,buttonAI,buttonNew]
