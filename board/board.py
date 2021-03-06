import random
import numpy as np
from animate.animate import anime


# block类，主要为了更方便的实现动画，可以存储上一个位置和动画类型，从而方便生成动画
class Block:
    def __init__(self, num, pos, animeType=0) -> None:
        self.num = num
        self.lastPos = pos
        self.anotherPos = [-1, -1]
        self.animate = anime((0, 0), (0, 0), 0)
        self.anotherAnimate = anime((0, 0), (0, 0), 0)
        self.animeType = animeType

    def addAnimate(self, startPos, endPos, totalTime, function=None):  # 添加动画，使用动画类进行操作
        if self.animate.startPos == startPos and self.animate.endPos == endPos:
            return
        else:
            if function == None:
                self.animate = anime(startPos, endPos, totalTime)
            else:
                self.animate = anime(startPos, endPos, totalTime, function)

    # 如果是合并类型，则需要给已经消失的块也添加一个动画
    def addAnotherAnimate(self, startPos, endPos, totalTime, function=None):
        if self.anotherAnimate.startPos == startPos and self.anotherAnimate.endPos == endPos:
            return
        else:
            if function == None:
                self.anotherAnimate = anime(startPos, endPos, totalTime)
            else:
                self.anotherAnimate = anime(
                    startPos, endPos, totalTime, function)

# TODO 将Broad改为任意矩形，将lineProcess归入Broad类


# 处理一行，这里的处理方式可能不是最优，但是对于实现动画是最方便的
def lineProcess(line):
    i = 0
    score = 0
    changed = False
    for i in range(len(line)):  # 将0聚集在尾部
        if(line[i].num == 0):
            k = i
            for j in range(i+1, len(line)):
                if(line[j].num != 0):
                    line[k] = line[j]
                    line[k].animeType = 1
                    changed = True
                    line[j] = Block(0, line[j].lastPos)
                    k += 1
            break
    for i in range(len(line)-1):  # 只需要到len-1即可，最后一位是不会合并的
        if line[i].num == 0:   # 已经将0转移至尾，如果扫到0则证明已经结束
            break
        else:
            if line[i].num == line[i+1].num:  # 如果相同则合并
                line[i+1].anotherPos = line[i].lastPos
                line[i] = line[i+1]
                line[i].animeType = 2
                line[i].num *= 2
                score += line[i].num
                changed = True
                k = i+1
                for j in range(i+2, len(line)):  # 合并后将后面数据前移
                    if(line[j].num != 0):
                        line[k] = line[j]
                        line[k].animeType = 1
                        line[j] = Block(0, line[j].lastPos)
                        k += 1
                if k == i+1:
                    line[i+1] = Block(0, line[i+1].lastPos)
    return line, changed, score


# board类，用于对棋盘进行各种处理，移动，添加，删除等，并添加了一些方便操作的函数
class Board:
    def __init__(self, size, map=None, score=0):
        self.size = size
        self.score = score
        self.debug = False
        self.changed = False
        self.map = np.array([[Block(0, [i, j])
                              for i in range(size)] for j in range(size)], dtype=Block)
        self.add()  # 随机产生第一个随机数
        self.add()  # 随机产生第二个随机数
        if isinstance(map, list) or isinstance(map, np.ndarray):
            for i in range(size):
                for j in range(size):
                    self.map[i][j] = Block(map[i][j].num, [i, j])

    def numMap(self):
        return [[self.map[i, j].num for j in range(self.size)] for i in range(self.size)]

    def mapPrint(self):
        for j in range(self.size):
            for i in range(self.size):  # 因为是先行后列，所以i放在后面
                print(self.map[i][j].num, end=' || ')
            print()
        print()

    def isChanged(self):
        if self.changed:
            self.changed = False
            return True
        return False

    # 新增2或4，有1/4概率产生4
    def add(self):
        if self.debug:
            print(self.numMap())
        tempList = []
        # 判断数值矩阵中是否有零
        for r in range(self.size):
            for c in range(self.size):
                if self.map[r][c].num == 0:
                    tempList.append([r, c])

        if len(tempList) > 0:
            [r, c] = random.choice(tempList)
            x = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])  # 随机产生一个 2 或 4
            self.map[r][c] = Block(x, [r, c], 3)  # 设置该坐标为随机值
            return True
        else:
            return False

    def add_xy(self, x, y, val):  # 在指定位置放置指定数字，用于AI
        if self.map[x][y].num == 0:
            self.map[x][y] = Block(val, [x, y], 3)
            return True
        else:
            return False

    def remove_xy(self, x, y):  # 删除指定位置的数字，用于AI
        self.map[x][y] = Block(0, [x, y])

    def move(self, dir):
        if dir == 0:
            return self.move_up()
        elif dir == 1:
            return self.move_down()
        elif dir == 2:
            return self.move_left()
        elif dir == 3:
            return self.move_right()

    # 向上计算
    def move_up(self):
        self.changed = False
        newLines = []
        thisScore = 0
        for i in range(self.size):
            tempLine, tempChanged, tempScore = lineProcess(
                self.map[i, :])  # 将map拆分成line进行处理
            thisScore += tempScore
            newLines.append(tempLine)
            self.changed = self.changed or tempChanged
        self.score += thisScore
        if self.changed:  # 发生改变
            newMap = np.vstack((newLines[0], newLines[1]))
            for i in range(2, len(newLines)):
                newMap = np.vstack((newMap, newLines[i]))
            self.map = newMap
        if self.debug:
            self.mapPrint()
        return self, self.changed, thisScore

    # 向下计算
    def move_down(self):
        self.changed = False
        newLines = []
        thisScore = 0
        for i in range(self.size):
            tempLine, tempChanged, tempScore = lineProcess(
                self.map[i, ::-1])  # 将map拆分成line进行处理
            thisScore += tempScore
            newLines.append(tempLine)
            self.changed = self.changed or tempChanged
        self.score += thisScore
        if self.changed:  # 发生改变
            newMap = np.vstack((newLines[0][::-1], newLines[1][::-1]))
            for i in range(2, len(newLines)):
                newMap = np.vstack((newMap, newLines[i][::-1]))
            self.map = newMap
        if self.debug:
            self.mapPrint()
        return self, self.changed, thisScore

    # 向左计算
    def move_left(self):
        self.changed = False
        newLines = []
        thisScore = 0
        for i in range(self.size):
            tempLine, tempChanged, tempScore = lineProcess(
                self.map[:, i])  # 将map拆分成line进行处理
            thisScore += tempScore
            newLines.append(tempLine)
            self.changed = self.changed or tempChanged
        self.score += thisScore
        if self.changed:  # 发生改变
            newMap = np.hstack(
                (np.transpose([newLines[0]]), np.transpose([newLines[1]])))
            for i in range(2, len(newLines)):
                newMap = np.hstack((newMap, np.transpose([newLines[i]])))
            self.map = newMap
        if self.debug:
            self.mapPrint()
        return self, self.changed, thisScore

    # 向右计算
    def move_right(self):
        self.changed = False
        newLines = []
        thisScore = 0
        for i in range(self.size):
            tempLine, tempChanged, tempScore = lineProcess(
                self.map[::-1, i])  # 将map拆分成line进行处理
            thisScore += tempScore
            newLines.append(tempLine)
            self.changed = self.changed or tempChanged
        self.score += thisScore
        if self.changed:  # 发生改变
            newMap = np.hstack(
                (np.transpose([newLines[0][::-1]]), np.transpose([newLines[1][::-1]])))
            for i in range(2, len(newLines)):
                newMap = np.hstack((newMap, np.transpose([newLines[i][::-1]])))
            self.map = newMap
        if self.debug:
            self.mapPrint()
        return self, self.changed, thisScore

    # 判断游戏结束
    def over(self):
        # 判断数值矩阵中是否有零
        for r in range(self.size):
            for c in range(self.size):
                if self.map[r][c].num == 0:
                    return False
        # 判断是否可以左右相消
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.map[r][c].num == self.map[r][c + 1].num:
                    return False
        # 判断是否可以上下相消
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.map[r][c].num == self.map[r + 1][c].num:
                    return False
        # print("游戏结束")
        return True

    def getAvailableCells(self):  # 返回所有的可以放数字的位置
        AvCells = []
        numMap = self.numMap()
        for i in range(self.size):
            for j in range(self.size):
                if numMap[i][j] == 0:
                    AvCells.append([i, j])
        return AvCells
