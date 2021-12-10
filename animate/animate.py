import numbers
import numpy as np


def newton(f, x=0.5, target=0, max=100, err=0.0001):
    n = 0
    while n < max:
        fx = f(x)
        if fx-target < err and fx-target > -err:
            return x
        else:
            diff = (f(x+err)-fx)/err
            x = x-(fx-target)/diff
        n += 1
    return None


def myCubicBezier(x, P1=[0.77, 0], P2=[0.175, 1]):

    ax = 3 * P1[0] - 3 * P2[0] + 1
    bx = 3 * P2[0] - 6 * P1[0]
    cx = 3 * P1[0]

    ay = 3 * P1[1] - 3 * P2[1] + 1
    by = 3 * P2[1] - 6 * P1[1]
    cy = 3 * P1[1]

    t = newton(lambda t: ((ax * t + bx) * t + cx) * t, x, x)

    return ((ay * t + by) * t + cy) * t


def mySigmode(x, scale=10):
    return 1/(1+np.exp(-(x-0.5)*scale))


def mySin(x):
    return 0.5*np.sin((x-0.5)*np.pi)+0.5


def smoothMove(startPos, endPos, nowTime, totalTime, function=mySigmode):
    if isinstance(startPos, numbers.Number) and isinstance(endPos, numbers.Number):
        return (endPos-startPos)*(function(nowTime/totalTime))+startPos
    elif isinstance(startPos, list) and isinstance(endPos, list):
        return [int(startPos[i]+(endPos[i]-startPos[i])*(function(nowTime/totalTime))+0.5) for i in range(0, len(startPos))]
    elif isinstance(startPos, tuple) and isinstance(endPos, tuple):
        return tuple((int(startPos[i]+(endPos[i]-startPos[i])*(function(nowTime/totalTime))+0.5) for i in range(0, len(startPos))))


class anime:
    def __init__(self, startPos, endPos, totalTime, func=myCubicBezier) -> None:
        self.startPos = startPos
        self.endPos = endPos
        self.totalTime = totalTime
        self.func = func
        self.finished = False
        self.nowTime = 0

    def PosNow(self, nowTime):
        if isinstance(self.startPos, numbers.Number) and isinstance(self.endPos, numbers.Number):
            return (self.endPos-self.startPos)*(self.func(nowTime/self.totalTime))+self.startPos
        elif isinstance(self.startPos, list) and isinstance(self.endPos, list):
            return [int(self.startPos[i]+(self.endPos[i]-self.startPos[i])*(self.func(nowTime/self.totalTime))+0.5) for i in range(0, len(self.startPos))]
        elif isinstance(self.startPos, tuple) and isinstance(self.endPos, tuple):
            return tuple((int(self.startPos[i]+(self.endPos[i]-self.startPos[i])*(self.func(nowTime/self.totalTime))+0.5) for i in range(0, len(self.startPos))))

    def move(self):
        Pos = self.PosNow(self.nowTime)
        if not self.finished:
            self.nowTime += 1
            if self.nowTime > self.totalTime:
                self.finished = True
        return Pos
