import random
import sys
import pygame
from pygame.locals import *
import time 
import val

Pixel = 90
size_x = 4
size_y = 4
PIXEL = 90
SIZE = 4
score_pixel = 100


class Board:
    def __init__(self, size,mapp):
        self.size = size
        self.score = 0
        self.map = [[0 for i in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                self.map[i][j]=mapp[i][j]
        #self.add()
        #self.add()
    def init_map(self):
        self.map = [[0 for i in range(self.size)] for i in range(self.size)]
      # 新增2或4，有1/4概率产生4
    def add(self):
        choose= [2,2,2,4]
        while True:
            r = random.randint(0,self.size - 1)
            c = random.randint(0,self.size - 1)
            if self.map[r][c] == 0:
                x = choose[random.randint(0 , 3)]
                self.map[r][c] = x
                break
    def add_xy(self,x,y,val):
        if self.map[x][y]==0:
            self.map[x][y]=val
            return True
        else:
            return False
    def move_up(self):
        changed=0
        for c in range(self.size):
            new = []
            bottom = 0
            for r in range(self.size):
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
                    if self.map[r][c] != new[r]:
                        changed=1
                    self.map[r][c] = new[r]
                else:
                    if self.map[r][c] != 0:
                        changed=1
                    self.map[r][c] = 0
        if changed > 0:
            return True,self
        else:
            return False,self
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
            return True,self
        else:
            return False,self
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
            return True,self
        else:
            return False,self
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
            return True,self
        else:
            return False,self
  # 逆时针旋转地图90度

  # 判断游戏结束
    def over(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.map[r][c] == 0:
                    return False
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.map[r][c] == self.map[r][c + 1]:
                    return False
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.map[r][c] == self.map[r + 1][c]:
                    return False
        print("game is over")
        return True



def show(board):
    my_word_color = (106, 90, 205)
    for i in range(size_x):
        for j in range(size_y):
            # 背景颜色块
            board_word_data =  board.map[i][j]
            screen_display.blit(board_word_data == 0 and block_display[(i + j) % 2] or block_display[2 + (i + j) % 2], (Pixel * j, Pixel * i))
            # 数值显示
            if board_word_data != 0:
                board_word = board_front.render(str(board_word_data), True, my_word_color)
                board_rect = board_word.get_rect()
                board_rect.center = (Pixel*j+Pixel/2,Pixel*i+Pixel/2)
                screen_display.blit(board_word,board_rect)
    # 分数显示
    screen_display.blit(score_get_block,(0,Pixel*size_y))#得分显示于左上角
    if board.over() == True:
        score_word = score_front.render('Game over',True,my_word_color)
    else:
        score_word = score_front.render('  Score:'+str(board.score),True,my_word_color)
    board_word = score_word.get_rect()
    board_word.center = (Pixel,Pixel*size_y+Pixel/2)
    screen_display.blit(score_word, board_word)
    #虚拟按钮显示
    screen_display.blit(start_get_block,(Pixel*2,Pixel*size_y))#得分显示于左上角
    start_word = start_front.render('start',True,my_word_color)
    board_word = start_word.get_rect()
    board_word.center = (Pixel*3,Pixel*size_y+Pixel/2)
    screen_display.blit(start_word, board_word)
    pygame.display.update()


def tip(board):
    for i in range(1):
        can_move = [True for i in range(4)]
        move = [board for i in range(4)]
        new = Board(SIZE , board.map)
        can_move,move[0] = new.move_up()
        if can_move:
            return 0
        new=Board(SIZE , board.map)
        can_move,move[1] = new.move_down()
        if can_move:
            return 1
        new=Board(SIZE , board.map)
        can_move,move[2] = new.move_left()
        if can_move:
            return 2
        new=Board(SIZE , board.map)
        can_move,move[3] = new.move_right()
        if can_move:
            return 3
    return 4

pygame.init()

#主体窗口设置
screen_display = pygame.display.set_mode((Pixel * size_x, Pixel * size_x + score_pixel))
block_display = [pygame.Surface((Pixel, Pixel)) for i in range(4)]

#棋盘颜色设置
block_display[0].fill((160, 150, 150))
block_display[1].fill((240, 255, 255))
block_display[2].fill((0, 255, 127))
block_display[3].fill((225, 255, 255))

#得分颜色设置
score_get_block = pygame.Surface((Pixel * size_x, score_pixel))
score_get_block.fill((245, 245, 245))
 
#开始颜色设置
start_get_block = pygame.Surface((Pixel * size_x, score_pixel))
start_get_block.fill((245, 245, 245))

#字体设置
start_front = pygame.font.Font(None, PIXEL * 2 // 3)
board_front = pygame.font.Font(None, PIXEL * 2 // 3)               
score_front = pygame.font.Font(None, Pixel * 2 // 3)




clock = pygame.time.Clock()
blank=[[0 for i in range(SIZE)] for i in range(SIZE)]
board = Board(SIZE , blank)
board.add()
board.add()
show(board)

while not board.over():
    clock.tick(12)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            #sys.exit()
    #接收玩家操作
    now_tip=tip(board)
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_w] or pressed_keys[K_UP]:
        board.move_up()
        board.add()
        time.sleep(0.15)
    elif pressed_keys[K_s] or pressed_keys[K_DOWN]:
        board.move_down()
        board.add()
        time.sleep(0.15)
    elif pressed_keys[K_a] or pressed_keys[K_LEFT]:
        board.move_left()
        board.add()
        time.sleep(0.15)
    elif pressed_keys[K_d] or pressed_keys[K_RIGHT]:
        board.move_right()
        board.add()
        time.sleep(0.15)
    elif pressed_keys[K_ESCAPE] :
        break
    show(board)


show(board)
    
while True:
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE] :
        break

pygame.quit()
print("游戏结束")
# 游戏结束
pygame.time.delay(3000)
