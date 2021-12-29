from numpy import result_type
import game.val as val
import pygame
from board import *
from pygame.locals import *
from show.show import *
import time
from sound.sound import *
from game.map import AIMap

search_step = 3
size_x = size_y = SIZE = 4


# 定义搜索结果类，用于方便处理返回值
class searchResult:
    def __init__(self, move=-1, score=0, positions=0, cutoffs=0) -> None:
        self.move = move
        self.positions = positions
        self.cutoffs = cutoffs
        self.score = score


# 四个方向向量，方便遍历时使用
vectors = [[0, 1], [1, 0], [-1, 0], [0, -1]]


# # 用于计算islands的类，这个不容易写成函数，直接写成类了
# class map:
#     def __init__(self, numMap: list) -> None:
#         self.map = numMap
#         self.marked = []

#     def islands(self):  # 计算分散度，越分散得分越高
#         islandsMark = 0
#         self.marked = [[True]*4]*4
#         for i in range(4):
#             for j in range(4):
#                 if self.map[i][j] != 0:
#                     self.marked[i][j] = False
#         for i in range(4):
#             for j in range(4):
#                 if self.map[i][j] != 0 and not self.marked[i][j]:
#                     islandsMark += 1
#                     self.mark(i, j, self.map[i][j])
#         return islandsMark

#     def mark(self, x, y, value):
#         if x >= 0 and x <= 3 and y >= 0 and y <= 3 and self.map[x][y] != 0 and self.map[x][y] == value and not self.marked[x][y]:
#             self.marked[x][y] = True
#             for direction in range(4):
#                 vector = vectors[direction]
#                 self.mark(x+vector[0], y+vector[1], value)


#
def search(thisBoard: AIMap, depth, alpha, beta, positions, cutoffs, plyaerTurn: bool) -> searchResult:
    """
    搜索最优移动方向
    功能:
        使用minmax搜索，并使用alpha，beta剪枝减少搜索次数
    参数:
        board:实例board界面
        depth:搜索深度
        alpha,beta:剪枝所需的参数
        positions,cutoffs:用于记录位置与剪枝次数
    返回值:
        searchResult:包含各种参数,详见searchResult类
    """
    bestScore = 0
    bestMove = -1
    result = searchResult()

    if plyaerTurn:  # max轮
        bestScore = alpha  # 最高分为alpha
        for direction in range(4):  # 四个方向分别进行遍历
            newBoard = AIMap(4, thisBoard.map)  # 新建一个棋盘防止影响到正式游戏
            changed = newBoard.move(direction)  # 相对应方向移动
            if changed:  # 如果这个方向可以移动
                positions += 1  # positions自增
                if depth == 0:  # 如果已经搜索到最底层了
                    result.move = direction
                    result.score = sum(val.evaluation(
                        newBoard.map))  # 返回当前局面的评价值
                else:  # 没有到达最深
                    result = search(
                        newBoard, depth-1, bestScore, beta, positions, cutoffs, False)  # 进行min轮，即让AI下出对局面最不利的一步
                    if result.score > 9900:  # 如果得分已经很高则适当减少
                        result.score -= 1
                    positions = result.positions
                    cutoffs = result.cutoffs  # 将返回值进行处理

                if result.score > bestScore:
                    bestScore = result.score
                    bestMove = direction
                if bestScore > beta:  # 如果最高值大于beta，则已经证明该走法优于前面的最优，则本深度下后面不用继续计算。
                    cutoffs += 1
                    return searchResult(bestMove, beta, positions, cutoffs)
    else:  # min轮，让AI走出最差一步
        bestScore = beta
        newBoard = AIMap(4, thisBoard.map)
        score_2 = []
        score_4 = []
        worstSituation = []
        cells = newBoard.getAvailableCells()
        for value in [2, 4]:  # 生成可能的所有情况，并进行评估
            for i in range(len(cells)):
                if not newBoard.add_xy(cells[i][0], cells[i][1], value):
                    print("!!!!")
                    input()
                if value == 2:
                    score_2.append(-val.smothness(newBoard.map) +
                                   newBoard.islands())
                if value == 4:
                    score_4.append(-val.smothness(newBoard.map) +
                                   newBoard.islands())
                newBoard.remove_xy(cells[i][0], cells[i][1])

        maxScore = max(max(score_2), max(score_4))  # 找到最差的情况
        for i in range(len(score_2)):  # 最差的情况可能不止一种，所以遍历一遍防止遗漏
            if score_2[i] == maxScore:
                worstSituation.append([cells[i], 2])
        for i in range(len(score_4)):
            if score_4[i] == maxScore:
                worstSituation.append([cells[i], 4])
        for situation in worstSituation:  # 遍历所有最差情况
            nnewBoard = AIMap(4, thisBoard.map)
            # input()
            if not nnewBoard.add_xy(situation[0][0], situation[0][1], situation[1]):
                print('nnewBoard.map', nnewBoard.map)
                print('newBoard.map', newBoard.map)
                print(situation)
                input()
            positions += 1
            result = search(nnewBoard, depth, alpha,
                            bestScore, positions, cutoffs, True)  # 进一步搜索
            positions = result.positions
            cutoffs = result.cutoffs

            if result.score < bestScore:
                bestScore = result.score

            if bestScore < alpha:  # 剪枝同理
                cutoffs += 1
                return searchResult(-1, alpha, positions, cutoffs)

    return searchResult(bestMove, bestScore, positions, cutoffs)


def getBestMove(board: Board, depth=4):
    """
    搜索最优移动方向
    功能:
        调用search,并给出参数
    参数:
        board:实例board界面
        depth:搜索深度
    返回值:
        最佳动作
    """
    nAIMap = AIMap(4, board.numMap())
    newBest = search(nAIMap, depth, -1000000, 1000000, 0, 0, True)
    return newBest.move


lastTime = int(time.time()*1000)


def AI_2048(board: Board, button, gap=50):
    """
    AI2048模式
    功能:
        根据pygame事件，进行AI游戏的上下左右移动和按键检测
    参数:
        board:实例board界面
        button:按键对象列表
        gap:AI算法速度，默认50
    返回值:
        GameState:默认为False，当判断New按键操作时为True重置board
    """
    global lastTime
    GameState = False
    if int(time.time()*1000) - lastTime > gap:
        lastTime = int(time.time()*1000)

        now = board
        operation = getBestMove(now)  # 调用AI算法
        print(operation)
        if operation == 0:
            board.move_up()
            slideSound()
            if(board.changed):
                board.add()  # 添加一个新数
        elif operation == 1:
            board.move_down()
            slideSound()
            if(board.changed):
                board.add()  # 添加一个新数
        elif operation == 2:
            board.move_left()
            slideSound()
            if(board.changed):
                board.add()  # 添加一个新数
        elif operation == 3:
            board.move_right()
            slideSound()
            if(board.changed):
                board.add()  # 添加一个新数

        # elif operation == -1:
        #     for i in range(4):
        #         board.move(i)
        #         if(board.changed):
        #             board.add()  # 添加一个新数
        #             break

    # 按键事件判断 #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # 直接退出
        button[0].check_event(event)
        button[1].check_event(event)
        button[2].check_event(event)
        GameState = button[3].check_event(event)

    return GameState


def testAIMap():
    tempMap = Board(4)
    while 1:
        print(tempMap.numMap())
        inDir = input()
        if inDir == 'w':
            tempMap.move_up()
        elif inDir == 's':
            tempMap.move_down()
        elif inDir == 'a':
            tempMap.move_left()
        elif inDir == 'd':
            tempMap.move_right()
