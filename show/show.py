from numpy.core.shape_base import block
import pygame
import math
from board import *

from show.showConfig import *


def index2pixel(indexPos):
    if isinstance(indexPos, list):
        return [indexPos[0]*Pixel, (indexPos[1]+2)*Pixel]
    elif isinstance(indexPos, tuple):
        return (indexPos[0]*Pixel, (indexPos[1]+2)*Pixel)


def showBotton(state):
    # 虚拟按钮显示
    if state == 1:
        screen_display.blit(button_block,(10,90))
        screen_display.blit(button_down_block,(13,93))
    elif state == 2:
        screen_display.blit(button_block,(100,90))
        screen_display.blit(button_down_block,(103,93))
    elif state == 3:
        screen_display.blit(button_block,(190,90))
        screen_display.blit(button_down_block,(193,93))
    elif state == 4:
        screen_display.blit(button_block,(280,90))  
        screen_display.blit(button_down_block,(283,93))
    else:
        screen_display.blit(button_up_block,(10,90))
        screen_display.blit(button_up_block,(100,90))
        screen_display.blit(button_up_block,(190,90))
        screen_display.blit(button_up_block,(280,90))

    base_word = start_front.render('Base', True, my_word_color)
    board_word = base_word.get_rect()  # 位置
    board_word.center = (45, Pixel+20)  # 居中显示
    screen_display.blit(base_word, board_word)  # 显示

    tip_word = start_front.render('Tip', True, my_word_color)
    board_word = tip_word.get_rect()  # 位置
    board_word.center = (135, Pixel+20)  # 居中显示
    screen_display.blit(tip_word, board_word)  # 显示

    ai_word = start_front.render('AI', True, my_word_color)
    board_word = ai_word.get_rect()  # 位置
    board_word.center = (225, Pixel+20)  # 居中显示
    screen_display.blit(ai_word, board_word)  # 显示

    newgame_word = start_front.render('New', True, my_word_color)
    board_word = newgame_word.get_rect()  # 位置
    board_word.center = (315, Pixel+20)  # 居中显示
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

def showTip(operation):
    
    tip_word = tip_front.render(
        tipWordMap[operation], True, my_word_color)
    board_word = tip_word.get_rect()  # 位置
    board_word.center = (180, 150)  # 居中显示
    screen_display.blit(tip_word, board_word)  # 显示


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


def slideProce(thisBlock: Block, posIndex, animateList: list):
    if thisBlock.lastPos != posIndex:  # 如果位置对不上，即有新的动画
        thisBlock.addAnimate(index2pixel(
            thisBlock.lastPos), index2pixel(posIndex), animeFrame)  # 则生成新的动画
        thisBlock.lastPos = posIndex
    displayPos = thisBlock.animate.move()  # 根据动画获得方块所在位置

    if thisBlock.animeType == 2:  # 如果是合并动画，会有两个方块
        if thisBlock.anotherPos != posIndex:  # 如果两个方块都要动的话

            thisBlock.addAnotherAnimate(index2pixel(
                thisBlock.anotherPos), index2pixel(posIndex), animeFrame)
            # 根据动画获得方块所在位置
            anotherDisplayPos = thisBlock.anotherAnimate.move(
            )
        else:
            anotherDisplayPos = index2pixel(posIndex)
        board_word_data = int(thisBlock.num/2)  # 数字保持倍增前
        animateList.append(
            [anotherDisplayPos, board_word_data])
    elif thisBlock.animeType == 1:
        board_word_data = int(thisBlock.num)  # 普通滑动动画，保持数字不变

    animateList.append([displayPos, board_word_data])

    if thisBlock.animate.finished:  # 如果动画已经完成，lastPos改为当前位置
        thisBlock.animeType = 0


def showAll(board: Board, button, operation = 4):

    screen_display.blit(show_display[0], (0, 0))
    screen_display.blit(show_display[1], (0, Pixel * 2-5))
    screen_display.blit(show_display[2], (0, Pixel * 6))

    slideList = []
    for i in range(size_x):
        for j in range(size_y):  # 遍历数值块，处理动画
            screen_display.blit(
                block_display[0], index2pixel([i, j]))  # 绘制底色（空位）
            if board.map[i][j].num != 0:
                # if [i, j] != list(board.map[i][j].lastPos):
                # 如果不是零且lastPos不等于当前，证明需要滑动动画
                if board.map[i][j].animeType == 1 or board.map[i][j].animeType == 2:
                    slideProce(board.map[i][j], [i, j], slideList)
                # else:
                #     print('!debug!', board.map[i][j].animeType)
                #     print('!debug!', board.map[i][j].lastPos, [i, j])
                else:  # 不需要动画
                    board_word_data = board.map[i][j].num
                    displayPos = index2pixel([i, j])
                    showBlock(displayPos, board_word_data)

    # 最后绘制动画，防止在扫描过程中绘制动画导致的遮挡问题
    for [pos, num] in slideList:
        showBlock(pos, num)

    showScore(board)
    # showBotton(False)
    showOhters()
    showTip(operation)
    button[0].update(screen_display)
    button[1].update(screen_display)
    button[2].update(screen_display)
    button[3].update(screen_display)

    pygame.display.update()  # 更新显示

    return len(slideList)
