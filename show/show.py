import pygame
import math
from board import *

from show.showConfig import *


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
    _2048_word = my_2048_front.render('2048', True, my_word_color)
    board_word = _2048_word.get_rect()  # 位置
    board_word.center = (Pixel, Pixel/2)  # 居中显示
    screen_display.blit(_2048_word, board_word)  # 显示

    designer_word = designer_front.render(
        ('Designer:雷佳臻 赵广宇 王琪源 蒋晓天 何旭东'), True, my_word_color)
    board_word = designer_word.get_rect()  # 位置
    board_word.center = (180, 555)  # 居中显示
    screen_display.blit(designer_word, board_word)  # 显示


def showScore(board: Board):
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


def slideProce(board: Board, i, j, animateList):
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


def showAll(board: Board):

    screen_display.blit(show_display[0], (0, 0))
    screen_display.blit(show_display[1], (0, Pixel * 2-5))
    screen_display.blit(show_display[2], (0, Pixel * 6))

    slideList = []

    for i in range(size_x):
        for j in range(size_y):  # 遍历数值块，处理动画
            screen_display.blit(
                block_display[0], index2pixel([i, j]))  # 绘制底色（空位）
            if board.map[i][j].num != 0:
                if [i, j] != list(board.map[i][j].lastPos):  # 如果不是零且lastPos不等于当前，证明需要滑动动画
                    slideProce(board, i, j, slideList)
                else:  # 不需要动画
                    board_word_data = board.map[i][j].num
                    displayPos = index2pixel([i, j])
                    showBlock(displayPos, board_word_data)

    # 最后绘制动画，防止在扫描过程中绘制动画导致的遮挡问题
    for [pos, num] in slideList:
        showBlock(pos, num)

    showScore(board)
    showBotton()
    showOhters()

    pygame.display.update()  # 更新显示