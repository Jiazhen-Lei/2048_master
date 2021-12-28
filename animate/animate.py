import numbers
import numpy as np
from pygame.math import enable_swizzling


def newton(f, x=0.5, target=0, max=100, err=0.0001):  # 牛顿法寻找函数对应函数值的自变量值，用于解贝塞尔曲线的对应时间值
    n = 0
    while n < max:  # 当循环次数大于指定max的时候如果还没找到，则退出并返回None
        fx = f(x)
        if fx-target < err and fx-target > -err:  # 如果误差已经小于指定err值，则返回结果
            return x
        else:  # 否则继续迭代
            diff = (f(x+err)-fx)/err
            x = x-(fx-target)/diff
        n += 1
    return None


def myCubicBezier(x, P1=[0.77, 0], P2=[0.175, 1]):  # 三阶贝塞尔曲线的函数，用于产生各种缓动曲线。

    ax = 3 * P1[0] - 3 * P2[0] + 1
    bx = 3 * P2[0] - 6 * P1[0]
    cx = 3 * P1[0]

    ay = 3 * P1[1] - 3 * P2[1] + 1
    by = 3 * P2[1] - 6 * P1[1]
    cy = 3 * P1[1]

    # 前面只能产生参数曲线，但是对应的函数值和自变量的对应曲线则需要通过牛顿法寻找
    t = newton(lambda t: ((ax * t + bx) * t + cx) * t, x, x)

    return ((ay * t + by) * t + cy) * t


def mySigmode(x, scale=10):  # sigmode函数，也是一种缓动曲线
    return 1/(1+np.exp(-(x-0.5)*scale))


def mySin(x):
    return 0.5*np.sin((x-0.5)*np.pi)+0.5


# 定义的缓动的移动，输入起始，终点位置，总时间，当前时间以及对应的缓动函数，返回的是当前应在的位置
# 支持输入列表，元组，数字
def smoothMove(startPos, endPos, nowTime, totalTime, function=myCubicBezier):
    if isinstance(startPos, numbers.Number) and isinstance(endPos, numbers.Number):
        return (endPos-startPos)*(function(nowTime/totalTime))+startPos
    elif isinstance(startPos, list) and isinstance(endPos, list):
        return [int(startPos[i]+(endPos[i]-startPos[i])*(function(nowTime/totalTime))+0.5) for i in range(0, len(startPos))]
    elif isinstance(startPos, tuple) and isinstance(endPos, tuple):
        return tuple((int(startPos[i]+(endPos[i]-startPos[i])*(function(nowTime/totalTime))+0.5) for i in range(0, len(startPos))))

# 动画类，可以方便调用，并且支持nowTick自增


class anime:
    def __init__(self, startPos, endPos, totalTime, func=myCubicBezier) -> None:
        self.startPos = startPos
        self.endPos = endPos
        self.totalTime = totalTime
        self.func = func
        if totalTime == 0:
            self.finished = True
        else:
            self.finished = False
        self.nowTime = 0

    def PosNow(self, nowTime):  # 返回当前位置
        if isinstance(self.startPos, numbers.Number) and isinstance(self.endPos, numbers.Number):
            return (self.endPos-self.startPos)*(self.func(nowTime/self.totalTime))+self.startPos
        elif isinstance(self.startPos, list) and isinstance(self.endPos, list):
            return [int(self.startPos[i]+(self.endPos[i]-self.startPos[i])*(self.func(nowTime/self.totalTime))+0.5) for i in range(0, len(self.startPos))]
        elif isinstance(self.startPos, tuple) and isinstance(self.endPos, tuple):
            return tuple((int(self.startPos[i]+(self.endPos[i]-self.startPos[i])*(self.func(nowTime/self.totalTime))+0.5) for i in range(0, len(self.startPos))))

    def move(self):  # 返回位置的同时将nowtime自增
        Pos = self.PosNow(self.nowTime)
        if not self.finished:
            self.nowTime += 1
            if self.nowTime > self.totalTime:
                self.finished = True
        return Pos
