import random
from typing import List

# 四个方向向量，方便遍历时使用
vectors = [[0, 1], [1, 0], [-1, 0], [0, -1]]


class AIMap:
    def __init__(self, size=4, numMap: list = None):
        self.size = size
        self.score = 0
        self.map = [[0 for i in range(size)] for i in range(size)]
        self.add()  # 随机产生第一个随机数
        self.add()  # 随机产生第二个随机数
        self.marked = []
        if isinstance(numMap, list):
            self.map = [[numMap[i][j]
                         for i in range(size)] for j in range(size)]

    def islands(self):  # 计算分散度，越分散得分越高
        islandsMark = 0
        self.marked = [[True]*4]*4
        for i in range(4):
            for j in range(4):
                if self.map[i][j] != 0:
                    self.marked[i][j] = False
        for i in range(4):
            for j in range(4):
                if self.map[i][j] != 0 and not self.marked[i][j]:
                    islandsMark += 1
                    self.mark(i, j, self.map[i][j])
        return islandsMark

    def mark(self, x, y, value):
        if x >= 0 and x <= 3 and y >= 0 and y <= 3 and self.map[x][y] != 0 and self.map[x][y] == value and not self.marked[x][y]:
            self.marked[x][y] = True
            for direction in range(4):
                vector = vectors[direction]
                self.mark(x+vector[0], y+vector[1], value)

    def move(self, dir): # 为了配合，所以这里是乱的
        if dir == 0:
            return self.move_left()
        elif dir == 1:
            return self.move_right()
        elif dir == 2:
            return self.move_up()
        elif dir == 3:
            return self.move_down()

    def getAvailableCells(self):  # 返回所有的可以放数字的位置
        AvCells = []
        numMap = self.map
        for i in range(self.size):
            for j in range(self.size):
                if numMap[i][j] == 0:
                    AvCells.append([i, j])
        return AvCells

    # 新增2或4，有1/4概率产生4

    def add(self):
        while True:
            r = random.randint(0, self.size - 1)  # 随机产生一个横坐标
            c = random.randint(0, self.size - 1)  # 随机产生一个纵坐标
            if self.map[r][c] == 0:  # 判断该坐标处是否有数值，若存在表示已有数据，重新产生随机坐标
                x = random.randint(1, 2) * 2  # 随机产生一个 2 或 4
                self.map[r][c] = x  # 设置该坐标为随机值
                break

    def add_xy(self, x, y, val):
        if self.map[x][y] == 0:
            self.map[x][y] = val
            return True
        else:
            return False

    def remove_xy(self, x, y):
        self.map[x][y] = 0
    # 向上计算

    def move_up(self):
        changed = False
        for c in range(self.size):  # 遍历 c-列
            new = []  # 新列数值缓存
            bottom = 0
            # 计算该列新数值
            for r in range(self.size):  # 遍历 r-行
                if self.map[r][c] == 0:
                    continue
                else:
                    if bottom == self.map[r][c]:  # 该列存在第二个相同数值块，进行相消
                        new[-1] *= 2
                        self.score += new[-1]
                        bottom = 0
                    else:  # 找到该列第一个有数值的坐标
                        bottom = self.map[r][c]  # 缓存上一个数值
                        new.append(bottom)  # 生成新列
            # 移动该列
            for r in range(self.size):
                if r < len(new):
                    if self.map[r][c] != new[r]:  # 与原列不同，发生改变
                        changed = True
                    self.map[r][c] = new[r]
                else:
                    if self.map[r][c] != 0:
                        changed = True
                    self.map[r][c] = 0
        return changed
    # 向下计算

    def move_down(self):
        changed = False
        for c in range(self.size):
            new = []
            bottom = 0
            for r in reversed(range(self.size)):
                if self.map[r][c] == 0:
                    continue
                else:
                    if bottom == self.map[r][c]:
                        new[-1] *= 2
                        self.score += new[-1]
                        bottom = 0
                    else:
                        bottom = self.map[r][c]
                        new.append(bottom)
            for r in range(self.size):
                if r < len(new):
                    if self.map[self.size-1-r][c] != new[r]:
                        changed = True
                    self.map[self.size-1-r][c] = new[r]
                else:
                    if self.map[self.size-1-r][c] != 0:
                        changed = True
                    self.map[self.size-1-r][c] = 0
        return changed
    # 向左计算

    def move_left(self):
        changed = False
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
                        new.append(bottom)
            for c in range(self.size):
                if c < len(new):
                    if self.map[r][c] != new[c]:
                        changed = True
                    self.map[r][c] = new[c]
                else:
                    if self.map[r][c] != 0:
                        changed = True
                    self.map[r][c] = 0
        return changed
    # 向右计算

    def move_right(self):
        changed = False
        for r in range(self.size):
            new = []
            bottom = 0
            for c in reversed(range(self.size)):
                if self.map[r][c] == 0:
                    continue
                else:
                    if bottom == self.map[r][c]:
                        new[-1] *= 2
                        self.score += new[-1]
                        bottom = 0
                    else:
                        bottom = self.map[r][c]
                        new.append(bottom)
            for c in range(self.size):
                if c < len(new):
                    if self.map[r][self.size-1-c] != new[c]:
                        changed = True
                    self.map[r][self.size-1-c] = new[c]
                else:
                    if self.map[r][self.size-1-c] != 0:
                        changed = True
                    self.map[r][self.size-1-c] = 0
        return changed
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
