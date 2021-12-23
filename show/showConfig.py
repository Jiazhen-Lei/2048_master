import pygame

pygame.init()  # 在pygame.font.Font需要，所以需要先执行

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
              (239, 229, 219),  # 2
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

tipWordMap = [('Tip:'), #空
              ('Tip:UP'),  # 向上
              ('Tip:DOWN'), # 向下
              ('Tip:LEFT'), # 向左
              ('Tip:RIGHT')] # 向右

# 棋盘颜色设置
# 13个Suface实例块，略小于单元块大小，剩余的部分通过背景色实现边框填充
block_display = [pygame.Surface((Pixel-5, Pixel-5)) for i in range(13)]

for i in range(len(block_display)):
    block_display[i].fill(myColorMap[i])


# 主体窗口设置
screen_display = pygame.display.set_mode((Pixel * show_x, Pixel * designer_y))
show_display = [pygame.Surface((Pixel * show_x, Pixel * 2)), pygame.Surface(
    (Pixel * show_x, Pixel * size_y + 5)), pygame.Surface((Pixel * show_x, Pixel * 0.3))]
show_display[0].fill((250, 248, 239))  # 给背景填充颜色，乳白
show_display[1].fill((189, 177, 166))  # 给背景填充颜色，深灰
show_display[2].fill((250, 248, 239))  # 给背景填充颜色，乳白

# 得分部件设置
score_get_block = pygame.Surface((Pixel+10, 30))  # 得分实例
score_get_block.fill((189, 177, 166))  # 填充颜色

# 按钮部件设置
button_block = pygame.Surface((70,40))
button_block.fill((250, 248, 239)) 
button_up_block = pygame.Surface((70,40))
button_up_block.fill((238, 225, 201))
button_down_block = pygame.Surface((64,34))
button_down_block.fill((189, 177, 166))

# 字体设置，字体及大小
start_front = pygame.font.Font(None, PIXEL * 2 // 6)  # 按钮
board_front = pygame.font.Font(None, PIXEL * 2 // 3)  # 数值矩阵数值
score_front = pygame.font.Font(None, PIXEL * 2 // 8)  # 得分
my_2048_front = pygame.font.Font(None, PIXEL * 2 // 2)  # 2048
designer_front = pygame.font.Font('./font/SimSun.ttf', 15)
tip_front = pygame.font.Font(None, 25) #tip

my_word_color = (106, 90, 205)

animeFrame = 3