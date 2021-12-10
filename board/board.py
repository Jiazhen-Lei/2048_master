import random

class Board:
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.map = [[0 for i in range(size)] for i in range(size)]
        self.add()  # 随机产生第一个随机数
        self.add()  # 随机产生第二个随机数
    # 新增2或4，有1/4概率产生4

    def add(self):
        while True:
            r = random.randint(0, self.size - 1)  # 随机产生一个横坐标
            c = random.randint(0, self.size - 1)  # 随机产生一个纵坐标
            if self.map[r][c] == 0:  # 判断该坐标处是否有数值，若存在表示已有数据，重新产生随机坐标
                x = random.randint(1, 2) * 2  # 随机产生一个 2 或 4
                self.map[r][c] = x  # 设置该坐标为随机值
                break
    # 向上计算

    def move_up(self):
        changed = 0
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
                        changed = 1
                    self.map[r][c] = new[r]
                else:
                    if self.map[r][c] != 0:
                        changed = 1
                    self.map[r][c] = 0
        if changed > 0:  # 发生改变
            self.add()  # 添加一个新数
        return self
    # 向下计算

    def move_down(self):
        changed = 0
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
                        changed = 1
                    self.map[self.size-1-r][c] = new[r]
                else:
                    if self.map[self.size-1-r][c] != 0:
                        changed = 1
                    self.map[self.size-1-r][c] = 0
        if changed > 0:
            self.add()
        return self
    # 向左计算

    def move_left(self):
        changed = 0
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
                        changed = 1
                    self.map[r][c] = new[c]
                else:
                    if self.map[r][c] != 0:
                        changed = 1
                    self.map[r][c] = 0
        if changed > 0:
            self.add()
        return self
    # 向右计算

    def move_right(self):
        changed = 0
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
                        changed = 1
                    self.map[r][self.size-1-c] = new[c]
                else:
                    if self.map[r][self.size-1-c] != 0:
                        changed = 1
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
