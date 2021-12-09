import sys
import game.base2048 as base
# import game.tip2048 as tip
# import game.ai2048 as ai
import pygame
from pygame.locals import *
import cv2
import math
import random
import time 

Pixel = 90 # 单元块像素个数
score_pixel = 100 # 得分显示区域纵像素个数
show_x = 4 # 主界面宽度
show_y = 6 # 主界面高度
size_x = 4 # 定义界面x宽度
size_y = 4 # 定义界面y高度
designer_y = 6.5
PIXEL = 90
SIZE = 4

# 运算功能
class Board:
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.map = [[0 for i in range(size)] for i in range(size)]
        self.add() # 随机产生第一个随机数
        self.add() # 随机产生第二个随机数 
    # 新增2或4，有1/4概率产生4
    def add(self):
        while True:
            r = random.randint(0,self.size - 1) # 随机产生一个横坐标
            c = random.randint(0,self.size - 1) # 随机产生一个纵坐标
            if self.map[r][c] == 0: # 判断该坐标处是否有数值，若存在表示已有数据，重新产生随机坐标
                x = random.randint(1 , 2) * 2 # 随机产生一个 2 或 4
                self.map[r][c] = x # 设置该坐标为随机值
                break
    # 向上计算
    def move_up(self):
        changed = 0
        for c in range(self.size): # 遍历 c-列
            new = [] # 新列数值缓存
            bottom = 0
            # 计算该列新数值
            for r in range(self.size): # 遍历 r-行
                if self.map[r][c] == 0:
                    continue
                else:
                    if bottom == self.map[r][c]: # 该列存在第二个相同数值块，进行相消
                        new[-1] *= 2
                        self.score+=new[-1]
                        bottom = 0
                    else: # 找到该列第一个有数值的坐标
                        bottom = self.map[r][c] # 缓存上一个数值
                        new.append( bottom ) # 生成新列
            # 移动该列
            for r in range(self.size):
                if r<len(new):
                    if self.map[r][c] != new[r]: # 与原列不同，发生改变
                        changed=1
                    self.map[r][c] = new[r]
                else:
                    if self.map[r][c] != 0:
                        changed=1
                    self.map[r][c] = 0
        if changed > 0: # 发生改变
            self.add() # 添加一个新数
        return self
    # 向下计算
    def move_down(self):
        changed=0
        for c in range(self.size):
            new = []
            bottom = 0
            for r in reversed(range(self.size)):
                if self.map[r][c] == 0:
                    continue
                else:
                    if bottom == self.map[r][c]:
                        new[-1] *= 2
                        self.score+=new[-1]
                        bottom = 0
                    else:
                        bottom = self.map[r][c]
                        new.append( bottom )
            for r in range(self.size):
                if r<len(new):
                    if self.map[self.size-1-r][c] != new[r]:
                        changed=1
                    self.map[self.size-1-r][c] = new[r]
                else:
                    if self.map[self.size-1-r][c] != 0:
                        changed=1
                    self.map[self.size-1-r][c] = 0      
        if changed > 0:
            self.add()
        return self   
    # 向左计算
    def move_left(self):
        changed=0
        for r in range(self.size):
            new = []
            bottom = 0
            for c in range(self.size):
                if self.map[r][c] == 0:
                    continue
                else:
                    if bottom == self.map[r][c]:
                        new[-1] *= 2
                        self.score += new[-1]
                        bottom = 0
                    else:
                        bottom = self.map[r][c]
                        new.append( bottom )
            for c in range(self.size):
                if c<len(new):
                    if self.map[r][c] != new[c]:
                        changed=1
                    self.map[r][c] = new[c]
                else:
                    if self.map[r][c] != 0:
                        changed=1
                    self.map[r][c] = 0 
        if changed > 0:
            self.add()
        return self
    # 向右计算
    def move_right(self):
        changed=0
        for r in range(self.size):
            new = []
            bottom = 0
            for c in reversed(range(self.size)):
                if self.map[r][c] == 0:
                    continue
                else:
                    if bottom == self.map[r][c]:
                        new[-1] *= 2
                        self.score+=new[-1]
                        bottom = 0
                    else:
                        bottom = self.map[r][c]
                        new.append( bottom )
            for c in range(self.size):
                if c<len(new):
                    if self.map[r][self.size-1-c] != new[c]:
                        changed=1
                    self.map[r][self.size-1-c] = new[c]
                else:
                    if self.map[r][self.size-1-c] != 0:
                        changed=1
                    self.map[r][self.size-1-c] = 0 
        if changed > 0:
            self.add()
        return self
    # 判断游戏结束
    def over(self):
        # 判断数值矩阵中是否有零
        for r in range(self.size):
            for c in range(self.size):
                if self.map[r][c] == 0:
                    return False
        # 判断是否可以左右相消
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.map[r][c] == self.map[r][c + 1]:
                    return False
        # 判断是否可以上限西
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.map[r][c] == self.map[r + 1][c]:
                    return False
        # print("游戏结束")
        return True

def show(board):
    my_word_color = (106, 90, 205)

    screen_display.blit(show_display[0],(0,0))
    screen_display.blit(show_display[1],(0,Pixel * 2-5))
    screen_display.blit(show_display[2],(0,Pixel * 6))

    for i in range(size_x):
        for j in range(size_y):
            # 背景颜色块
            board_word_data =  board.map[i][j] # 遍历数值块
              # 显示：第一个参数是块，第二个参数是坐标，是一个三目运算相当于if else
            screen_display.blit(board_word_data == 0 and block_display[0] or block_display[int(math.log(board_word_data,2))], (Pixel * j, Pixel * (i+2)))
            # 数值显示
            if board_word_data != 0:
                board_word = board_front.render(str(board_word_data), True, my_word_color) # 参数：内容，是否抗锯齿，颜色
                board_rect = board_word.get_rect() # 位置
                board_rect.center = (Pixel*j+Pixel/2,Pixel*(i+2)+Pixel/2) # 居中显示
                screen_display.blit(board_word,board_rect) # 显示
    # 分数显示
    screen_display.blit(score_get_block,(Pixel * 3-20,10)) # 显示块位置
    if board.over() == True: # 游戏结束
        score_word = score_front.render('Game over',True,my_word_color)
    else:
        score_word = score_front.render('  Score:'+str(board.score),True,my_word_color)
    board_word = score_word.get_rect() # 位置
    board_word.center = (Pixel * 3+20,Pixel/3-5) 
    screen_display.blit(score_word, board_word) # 显示

    #2048显示
    _2048_word = _2048_front.render('2048',True,my_word_color)
    board_word = _2048_word.get_rect() # 位置
    board_word.center = (Pixel,Pixel/2) # 居中显示
    screen_display.blit(_2048_word, board_word) # 显示

    #虚拟按钮显示
    base_word = start_front.render('Base',True,my_word_color)
    board_word = base_word.get_rect() # 位置
    board_word.center = (0+40,Pixel+20) # 居中显示
    screen_display.blit(base_word, board_word) # 显示
    
    tip_word = start_front.render('Tip',True,my_word_color)
    board_word = tip_word.get_rect() # 位置
    board_word.center = (Pixel+30,Pixel+20) # 居中显示
    screen_display.blit(tip_word, board_word) # 显示

    ai_word = start_front.render('AI',True,my_word_color)
    board_word = ai_word.get_rect() # 位置
    board_word.center = (Pixel*2+10,Pixel+20) # 居中显示
    screen_display.blit(ai_word, board_word) # 显示

    newgame_word = start_front.render('New Game',True,my_word_color)
    board_word = newgame_word.get_rect() # 位置
    board_word.center = (Pixel*3+20,Pixel+20) # 居中显示
    screen_display.blit(newgame_word, board_word) # 显示

    designer_word = designer_front.render(('Designer:雷佳臻 赵广宇 王琪源 蒋晓天 何旭东'),True,my_word_color)
    board_word = designer_word.get_rect() # 位置
    board_word.center = (180,555) # 居中显示
    screen_display.blit(designer_word, board_word) # 显示

    pygame.display.update() # 更新显示

pygame.init()

#主体窗口设置
screen_display = pygame.display.set_mode((Pixel * show_x, Pixel * designer_y ))
show_display = [pygame.Surface((Pixel * show_x, Pixel * 2 )),pygame.Surface((Pixel * show_x, Pixel * size_y + 5)),pygame.Surface((Pixel * show_x, Pixel * 0.3 ))]
show_display[0].fill((250, 248, 239)) # 给背景填充颜色，乳白
show_display[1].fill((189, 177, 166)) # 给背景填充颜色，深灰
show_display[2].fill((250, 248, 239)) # 给背景填充颜色，乳白
#棋盘颜色设置
block_display = [pygame.Surface((Pixel-5, Pixel-5)) for i in range(13)] # 13个Suface实例块，略小于单元块大小，剩余的部分通过背景色实现边框填充
block_display[0].fill((203, 193, 182)) # 0
block_display[1].fill((239, 229, 219)) # 2
block_display[2].fill((238, 225, 201)) # 4
block_display[3].fill((242, 179, 122)) # 8
block_display[4].fill((237, 142, 83)) # 16
block_display[5].fill((246, 125, 95)) # 32
block_display[6].fill((235, 89, 52)) # 64
block_display[7].fill((243, 217, 107)) # 128
block_display[8].fill((241, 209, 74)) # 256
block_display[9].fill((229, 193, 38)) # 512
block_display[10].fill((221, 185, 38)) # 1024
block_display[11].fill((213, 178, 38)) # 2048
block_display[12].fill((201, 163, 35)) # 4096

#得分部件设置
score_get_block = pygame.Surface((Pixel+10, 30)) # 得分实例
score_get_block.fill((189, 177, 166)) # 填充颜色

#字体设置，字体及大小
start_front = pygame.font.Font(None, PIXEL * 2 // 6) # 按钮
board_front = pygame.font.Font(None, PIXEL * 2 // 3) # 数值矩阵数值
score_front = pygame.font.Font(None, PIXEL * 2 // 8) # 得分
_2048_front = pygame.font.Font(None, PIXEL * 2 // 2) # 2048
designer_front = pygame.font.Font('./font/SimSun.ttf',15)

clock = pygame.time.Clock() # 系统时间
board = Board(SIZE) # 实例化board对象，传递参数size = 4 


def play():
    show(board) # 显示
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 退出
                pygame.quit()
            if MOUSEBUTTONDOWN == event.type:
                pressed_array = pygame.mouse.get_pressed() 
                if pressed_array[0] == 1:
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0] # x坐标
                    mouse_y = pos[1] # y坐标
                    if  40 < mouse_x < 90 and 90 < mouse_y < 130:
                        print("Start Base 2048")
                        while not board.over():
                            clock.tick(12)
                            base.start_base_2048(board,clock)
                            show(board)
                        print("游戏结束")
                        pygame.quit()
                        pygame.time.delay(2000)
                        break
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Start Tip 2048")
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Start AI 2048")
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Please choose your new mode")
                    else:continue
    

play()
