import sys
import game.base2048 as base
# import game.tip2048 as tip
# import game.ai2048 as ai
import pygame
from pygame.locals import *
import cv2



Pixel = 90
show_x = 4
show_y = 6

def show():
    my_word_color = (106, 90, 205)

    plane=pygame.image.load('./picture/img1.jpg')
    screen_display.blit(plane,(0,0))

    button_1 = pygame.image.load('./picture/img2.jpg')
    screen_display.blit(button_1,(Pixel*1.2, Pixel * 0.75))

    button_2 = pygame.image.load('./picture/img2.jpg')
    screen_display.blit(button_2,(Pixel*1.2, Pixel * 2.25))

    button_3 = pygame.image.load('./picture/img2.jpg')
    screen_display.blit(button_3,(Pixel*1.2, Pixel * 3.75))

    producer_img = pygame.image.load('./picture/img3.jpg')
    screen_display.blit(producer_img,(55, 500))

    producer = producer_front.render(('雷佳臻 赵广宇 王琪源'), True,(0,0,0))
    producer_rect = producer.get_rect()
    producer_rect.center = (180,515)
    screen_display.blit(producer,producer_rect)

    board_word = board_front.render(str('Base'), True, my_word_color)
    board_rect = board_word.get_rect()
    board_rect.center = (Pixel*2,Pixel*1)
    screen_display.blit(board_word,board_rect)

    board_word = board_front.render(str('Tip'), True, my_word_color)
    board_rect = board_word.get_rect()
    board_rect.center = (Pixel*2,Pixel*2.5)
    screen_display.blit(board_word,board_rect)

    board_word = board_front.render(str('AI'), True, my_word_color)
    board_rect = board_word.get_rect()
    board_rect.center = (Pixel*2,Pixel*4)
    screen_display.blit(board_word,board_rect)
    pygame.display.update()

    mouse_state = pygame.event.get()

pygame.init()

#主体窗口设置
screen_display = pygame.display.set_mode((Pixel * show_x, Pixel * show_y ))
block_display = pygame.Surface((Pixel*1.6, Pixel*0.8)) 
block_display.fill((249,246,242))

#界面字体设置
board_front = pygame.font.SysFont('arial', Pixel * 2//4)               
score_front = pygame.font.SysFont('华文宋体', Pixel * 2//4)
producer_front = pygame.font.Font('./font/SimSun.ttf',25)

def mode_get():
    show()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if MOUSEBUTTONDOWN == event.type:
                print('鼠标被按下了')
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0] == 1:
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0]
                    mouse_y = pos[1]
                    if 108<mouse_x<252 and 67<mouse_y<140:
                        return 1
                    if 108<mouse_x<252 and 202<mouse_y<275:
                        return 2
                    if 108<mouse_x<252 and 337<mouse_y<409:
                        return 3
        pygame.display.update()

def start_show():
    mode = 0
    mode = mode_get()
    if mode == 1:
        pygame.display.quit()
        base.base_2048()
    elif mode == 2:
        # tip.tip_2048()
        pass
    elif mode == 3:
        # ai.ai_2048()
        pass
    
start_show()
