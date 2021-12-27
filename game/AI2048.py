from numpy import result_type
import game.val as val
import pygame
from board import *
from pygame.locals import *
from show.show import *
import time
from sound.sound import *

search_step = 3
size_x = size_y = SIZE = 4


def worst_val(map):
    new = map.numMap()
    ansx = ansy = ansk = 0
    worst = [1000000]

    for i in range(size_x):
        for j in range(size_y):
            for k in range(1, 3):
                if new[i][j] > 0:
                    continue
                new[i][j] = k*2
                now_val = val.evaluation(new, map.score)
                if sum(now_val) < sum(worst):
                    worst, ansx, ansy, ansk = now_val, i, j, k*2
                new[i][j] = 0

    return worst, ansx, ansy, ansk


class searchResult:
    def __init__(self, move=-1, score=0, positions=0, cutoffs=0) -> None:
        self.move = move
        self.positions = positions
        self.cutoffs = cutoffs
        self.score = score


vectors = [[0, 1], [1, 0], [-1, 0], [0, -1]]


class map:
    def __init__(self, numMap: list) -> None:
        self.map = numMap
        self.marked = []

    def islands(self):
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


def search(thisBoard: Board, depth, alpha, beta, positions, cutoffs, plyaerTurn: bool) -> searchResult:
    bestScore = 0
    bestMove = -1
    result = searchResult()

    if plyaerTurn:
        bestScore = alpha
        for direction in range(4):
            newBoard = Board(4, thisBoard.map)
            _, changed, _ = newBoard.move(direction)
            if changed:
                positions += 1
                if depth == 0:
                    result.move = direction
                    result.score = sum(val.evaluation(newBoard.numMap()))
                else:
                    result = search(
                        newBoard, depth-1, bestScore, beta, positions, cutoffs, False)
                    if result.score > 9900:
                        result.score -= 1
                    positions = result.positions
                    cutoffs = result.cutoffs

                if result.score > bestScore:
                    bestScore = result.score
                    bestMove = direction
                if bestScore > beta:
                    cutoffs += 1
                    return searchResult(bestMove, beta, positions, cutoffs)
    else:
        bestScore = beta
        newBoard = Board(4, thisBoard.map)
        score_2 = []
        score_4 = []
        worstSituation = []
        cells = newBoard.getAvailableCells()
        for value in [2, 4]:
            for i in range(len(cells)):
                if not newBoard.add_xy(cells[i][0], cells[i][1], value):
                    print("!!!!")
                    input()
                if value == 2:
                    score_2.append(-val.smothness(newBoard.numMap()
                                                  )+map(newBoard.numMap()).islands())
                if value == 4:
                    score_4.append(-val.smothness(newBoard.numMap()
                                                  )+map(newBoard.numMap()).islands())
                newBoard.remove_xy(cells[i][0], cells[i][1])

        maxScore = max(max(score_2), max(score_4))
        for i in score_2:
            if i == maxScore:
                worstSituation.append([cells[score_2.index(i)], 2])
        for i in score_4:
            if i == maxScore:
                worstSituation.append([cells[score_4.index(i)], 4])

        for situation in worstSituation:
            nnewBoard = Board(4, thisBoard.map)
            nnewBoard.add_xy(situation[0][0], situation[0][1], situation[1])
            positions += 1
            result = search(nnewBoard, depth, alpha,
                            bestScore, positions, cutoffs, True)
            positions = result.positions
            cutoffs = result.cutoffs

            if result.score < bestScore:
                bestScore = result.score

            if bestScore < alpha:
                cutoffs += 1
                return searchResult(-1, alpha, positions, cutoffs)

    return searchResult(bestMove, bestScore, positions, cutoffs)


def getBestMove(board: Board, depth=3):
    newBest = search(board, depth, -1000000, 1000000, 0, 0, True)
    return newBest.move


def dfs(board: Board, now_step, limit_step):
    can_move = [True for i in range(4)]
    move = [board for i in range(4)]
    secondBest = []
    if now_step == 0:
        # if False:
        new = Board(SIZE, board.map)
        move[0], can_move[0], _ = new.move_up()
        new = Board(SIZE, board.map)
        move[1], can_move[1], _ = new.move_down()
        new = Board(SIZE, board.map)
        move[2], can_move[2], _ = new.move_left()
        new = Board(SIZE, board.map)
        move[3], can_move[3], _ = new.move_right()
    else:
        new = Board(SIZE, board.map, board.score)
        move[0], can_move[0], _ = new.move_up()
        new = Board(SIZE, board.map, board.score)
        move[1], can_move[1], _ = new.move_down()
        new = Board(SIZE, board.map, board.score)
        move[2], can_move[2], _ = new.move_left()
        new = Board(SIZE, board.map, board.score)
        move[3], can_move[3], _ = new.move_right()
    best_move = -1
    best_val = [-1]
    if now_step == limit_step:
        for i in range(4):
            if not can_move[i]:
                continue
            val_now, x, y, k = worst_val(move[i])
            val_now = [0] if sum(val_now) <= 0 else val_now
            if sum(val_now) > sum(best_val):
                best_move = i
                best_val = val_now
    else:
        for i in range(4):
            if not can_move[i]:
                continue
            val_now, x, y, k = worst_val(move[i])
            move[i].add_xy(x, y, k)
            now_move, val_now, blank_move = dfs(
                move[i], now_step+1, limit_step)
            # val_now = max(0, val_now)
            val_now = [0] if sum(val_now) <= 0 else val_now
            if sum(val_now) > sum(best_val):
                best_move = i
                secondBest = best_val
                best_val = val_now
    # print(now_step,best_move,best_val)
    # print(board.map)
    if now_step == 0:
        if len(best_val) == len(secondBest):
            print('             secondWin:', [
                best_val[i]-secondBest[i] for i in range(len(best_val))])
        print('operation=', best_move, 'best_val=', best_val)
        print(can_move)
    return best_move, best_val, can_move


lastTime = int(time.time()*1000)

def AI_2048(board: Board, button, gap=50):
    global lastTime
    GameState = False
    if int(time.time()*1000) - lastTime > gap:
        lastTime = int(time.time()*1000)
 
        now = board
        operation = getBestMove(now)

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
            # time.sleep(0.1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # 直接退出
        button[0].check_event(event)
        button[1].check_event(event)
        button[2].check_event(event)
        GameState = button[3].check_event(event)

    return GameState