import sys

from pygame import display
import game.base2048 as base
# import game.tip2048 as tip
# import game.ai2048 as ai
import pygame
from pygame.locals import *
import math
from board import *
import random
import time

Pixel = 90  # 单元块像素个数
score_pixel = 100  # 得分显示区域纵像素个数
show_x = 4  # 主界面宽度
show_y = 6  # 主界面高度
size_x = 4  # 定义界面x宽度
size_y = 4  # 定义界面y高度
designer_y = 6.5
PIXEL = 90
SIZE = 4

myColorMap = [(203, 193, 182),  # 0
              (203, 193, 182),  # 2
              (238, 225, 201),  # 4
              (242, 179, 122),  # 8
              (237, 142, 83),  # 16
              (246, 125, 95),  # 32
              (235, 89, 52),   # 64
              (243, 217, 107),  # 128
              (241, 209, 74),  # 256
              (229, 193, 38),  # 512
              (221, 185, 38),  # 1024
              (213, 178, 38),  # 2048
              (201, 163, 35)]   # 4096

my_word_color = (106, 90, 205)


def index2pixel(indexPos):
    if isinstance(indexPos, list):
        return [indexPos[0]*Pixel, (indexPos[1]+2)*Pixel]
    elif isinstance(indexPos, tuple):
        return (indexPos[0]*Pixel, (indexPos[1]+2)*Pixel)


def showBotton():
    # 虚拟按钮显示
    base_word = start_front.render('Base', True, my_word_color)
    board_word = base_word.get_rect()  # 位置
    board_word.center = (0+40, Pixel+20)  # 居中显示
    screen_display.blit(base_word, board_word)  # 显示

    tip_word = start_front.render('Tip', True, my_word_color)
    board_word = tip_word.get_rect()  # 位置
    board_word.center = (Pixel+30, Pixel+20)  # 居中显示
    screen_display.blit(tip_word, board_word)  # 显示

    ai_word = start_front.render('AI', True, my_word_color)
    board_word = ai_word.get_rect()  # 位置
    board_word.center = (Pixel*2+10, Pixel+20)  # 居中显示
    screen_display.blit(ai_word, board_word)  # 显示

    newgame_word = start_front.render('New Game', True, my_word_color)
    board_word = newgame_word.get_rect()  # 位置
    board_word.center = (Pixel*3+20, Pixel+20)  # 居中显示
    screen_display.blit(newgame_word, board_word)  # 显示


def showOhters():
    # 2048显示
    _2048_word = _2048_front.render('2048', True, my_word_color)
    board_word = _2048_word.get_rect()  # 位置
    board_word.center = (Pixel, Pixel/2)  # 居中显示
    screen_display.blit(_2048_word, board_word)  # 显示

    designer_word = designer_front.render(
        ('Designer:雷佳臻 赵广宇 王琪源 蒋晓天 何旭东'), True, my_word_color)
    board_word = designer_word.get_rect()  # 位置
    board_word.center = (180, 555)  # 居中显示
    screen_display.blit(designer_word, board_word)  # 显示


def showScore():
    # 分数显示
    screen_display.blit(score_get_block, (Pixel * 3-20, 10))  # 显示块位置
    if board.over() == True:  # 游戏结束
        score_word = score_front.render('Game over', True, my_word_color)
    else:
        score_word = score_front.render(
            '  Score:'+str(board.score), True, my_word_color)
    board_word = score_word.get_rect()  # 位置
    board_word.center = (Pixel * 3+20, Pixel/3-5)
    screen_display.blit(score_word, board_word)  # 显示


def showNum(board_word_data, disPos):
    # 数值显示
    if board_word_data != 0:
        board_word = board_front.render(
            str(board_word_data), True, my_word_color)  # 参数：内容，是否抗锯齿，颜色
        board_rect = board_word.get_rect()  # 位置
        board_rect.center = (disPos[0]+Pixel/2, disPos[1]+Pixel/2)  # 居中显示
        screen_display.blit(board_word, board_rect)  # 显示


def showBlock(pos, num=0):
    screen_display.blit(
        block_display[0 if num == 0 else min(int(math.log(num, 2)), 12)], pos)
    showNum(num, pos)


def slideProce(board, i, j, animateList):
    board.map[i][j].addAnimate(index2pixel(
        board.map[i][j].lastPos), index2pixel([i, j]), 10)
    if board.map[i][j].animate.finished:  # 如果动画已经完成，lastPos改为当前位置
        board.map[i][j].lastPos = [i, j]
    displayPos = board.map[i][j].animate.move()  # 根据动画获得方块所在位置

    if board.map[i, j].moveType == 1:  # 如果是合并动画，会有两个方块
        if board.map[i][j].anotherPos != [i, j]:  # 如果两个方块都要动的话
            board.map[i, j].addAnotherAnimate(index2pixel(
                board.map[i][j].anotherPos), index2pixel([i, j]), 10)
            # 根据动画获得方块所在位置
            anotherDisplayPos = board.map[i][j].anotherAnimate.move(
            )
        else:
            anotherDisplayPos = index2pixel([i, j])
        board_word_data = int(board.map[i][j].num/2)  # 数字保持倍增前
        animateList.append(
            [anotherDisplayPos, board_word_data])
    else:
        board_word_data = int(board.map[i][j].num)  # 普通滑动动画，保持数字不变

    animateList.append([displayPos, board_word_data])


def show(board):

    screen_display.blit(show_display[0], (0, 0))
    screen_display.blit(show_display[1], (0, Pixel * 2-5))
    screen_display.blit(show_display[2], (0, Pixel * 6))

    slideList = []

    for i in range(size_x):
        for j in range(size_y):  # 遍历数值块，处理动画
            screen_display.blit(
                block_display[0], index2pixel([i, j]))  # 绘制底色（空位）
            if board.map[i][j].num != 0:
                if [i, j] != board.map[i][j].lastPos:  # 如果不是零且lastPos不等于当前，证明需要滑动动画
                    slideProce(board, i, j, slideList)
                else:  # 不需要动画
                    board_word_data = board.map[i][j].num
                    displayPos = index2pixel([i, j])
                    showBlock(displayPos, board_word_data)

    # 最后绘制动画，防止在扫描过程中绘制动画导致的遮挡问题
    for [pos, num] in slideList:
        showBlock(pos, num)

    showScore()
    showBotton()
    showOhters()

    pygame.display.update()  # 更新显示


pygame.init()

# 主体窗口设置
screen_display = pygame.display.set_mode((Pixel * show_x, Pixel * designer_y))
show_display = [pygame.Surface((Pixel * show_x, Pixel * 2)), pygame.Surface(
    (Pixel * show_x, Pixel * size_y + 5)), pygame.Surface((Pixel * show_x, Pixel * 0.3))]
show_display[0].fill((250, 248, 239))  # 给背景填充颜色，乳白
show_display[1].fill((189, 177, 166))  # 给背景填充颜色，深灰
show_display[2].fill((250, 248, 239))  # 给背景填充颜色，乳白
# 棋盘颜色设置
# 13个Suface实例块，略小于单元块大小，剩余的部分通过背景色实现边框填充
block_display = [pygame.Surface((Pixel-5, Pixel-5)) for i in range(13)]

for i in range(len(block_display)):
    block_display[i].fill(myColorMap[i])

# 得分部件设置
score_get_block = pygame.Surface((Pixel+10, 30))  # 得分实例
score_get_block.fill((189, 177, 166))  # 填充颜色

# 字体设置，字体及大小
start_front = pygame.font.Font(None, PIXEL * 2 // 6)  # 按钮
board_front = pygame.font.Font(None, PIXEL * 2 // 3)  # 数值矩阵数值
score_front = pygame.font.Font(None, PIXEL * 2 // 8)  # 得分
_2048_front = pygame.font.Font(None, PIXEL * 2 // 2)  # 2048
designer_front = pygame.font.Font('./font/SimSun.ttf', 15)

clock = pygame.time.Clock()  # 系统时间
board = Board(SIZE)  # 实例化board对象，传递参数size = 4

# board.map=[[2]*4,[0]*4,[0]*4,[0]*4]


def play():
    show(board)  # 显示
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
            if MOUSEBUTTONDOWN == event.type:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0] == 1:
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0]  # x坐标
                    mouse_y = pos[1]  # y坐标
                    if 40 < mouse_x < 90 and 90 < mouse_y < 130:
                        print("Start Base 2048")
                        while not board.over():
                            clock.tick(60)
                            base.start_base_2048(board, clock)
                            show(board)
                        print("游戏结束")
                        # TODO 增加结束界面
                        pygame.quit()
                        pygame.time.delay(2000)
                        break
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Start Tip 2048")
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Start AI 2048")
                    elif 220 < mouse_x < 320 and 380 < mouse_y < 440:
                        print("Please choose your new mode")
                    else:
                        continue


if __name__ == '__main__':
    play()
