import math


def evaluation(map, score=0):
    # smoothWeight = 0.001  # 0.5
    # mono2Weight = 0.001  # 0.03
    # emptyWeight = 5  # 2.7
    # maxWeight = 1  # 0.01
    # disWeight = 0.5
    # smoothWeight = 0.3  # 0.5
    # mono2Weight = 0.5  # 0.03
    # emptyWeight = 0  # 2.7
    # maxWeight = 1  # 0.01
    # disWeight = 0.5
    smoothWeight = 0.5  # 0.5
    mono2Weight = 1  # 0.03
    emptyWeight = 5  # 2.7
    maxWeight = 1  # 0.01
    disWeight = 0.01

    result = [disWeight*dis_weight(map), smoothWeight * smothness(map), mono2Weight *
              monotonicity(map), emptyWeight*empty_num(map), maxWeight*max_num(map), score]
    return result


def dis_weight(map):
    # wei=[[100,10,10,100],
    #     [10,1,1,10],
    #     [10,1,1,10],
    #     [100,10,10,100]]
    wei = [[12, 13, 25, 50],
           [11, 10, 9, 8],
           [4, 5, 6, 7],
           [3, 2, 1, 0]]
    dis_sum = 0
    for j in range(4):
        for i in range(4):
            if map[i][j] == 0:
                continue
            dis_sum += math.log2(map[i][j])*wei[i][j]
    return dis_sum


def empty_num(map):
    empty_num = 0
    for i in range(4):
        for j in range(4):
            if map[i][j] == 0:
                empty_num += 1
    return empty_num


def max_num(map):
    max_num = 0
    for i in range(4):
        for j in range(4):
            if max_num < map[i][j]:
                max_num = map[i][j]
    return max_num


def smothness(map):
    lubricity = 0
    for i in range(4):
        for j in range(4):
            if i >= 1:
                # 左边减去该值
                lubricity += abs(math.log2(map[i-1]
                                 [j]+1) - math.log2(map[i][j]+1))
            if i < 3:
                # 右边减去该值
                lubricity += abs(math.log2(map[i+1]
                                 [j]+1) - math.log2(map[i][j]+1))
            if j > 0:
                # 上面减去该值
                lubricity += abs(math.log2(map[i]
                                 [j-1]+1) - math.log2(map[i][j]+1))
            if j < 3:
                # 下面减去该值
                lubricity += abs(math.log2(map[i]
                                 [j+1]+1) - math.log2(map[i][j]+1))
    return lubricity


# def smothness(map):
#     lubricity = 0
#     for i in range(4):
#         for j in range(3):
#             if map[i][j] == 0 or map[i][j+1] == 0:
#                 continue
#             lubricity += abs(math.log2(map[i][j+1]+1) - math.log2(map[i][j]+1))
#     for i in range(3):
#         for j in range(4):
#             if map[i][j] == 0 or map[i+1][j] == 0:
#                 continue
#             lubricity += abs(math.log2(map[i+1][j]+1) - math.log2(map[i][j]+1))
#     return lubricity


def monotonicity(map):
    totals = [0, 0]  # totals【0】储存单调增加，totals[1]储存单调递减
    # up/down direction
    # add

    for i in range(4):
        now = []
        for j in range(4):
            if map[i][j] == 0:
                continue
            now.append(map[i][j])
        if len(now) == 0:
            continue
        if sorted(now) == now:
            totals[0] += 1
    for j in range(4):
        now = []
        for i in range(4):
            if map[i][j] == 0:
                continue
            now.append(map[i][j])
        if len(now) == 0:
            continue
        if sorted(now) == now:
            totals[1] += 1
    return max(totals)


'''
def  monotonicity(map):
    totals = [0, 0]#totals【0】储存单调增加，totals[1]储存单调递减
    #up/down direction
    #add
    num_1_pre = 0
    for i in range(4):
        for j in range(3):
            if map[i][j]!=0:
                num_1_now = map[i][j]
            else:
                num_1_now = num_1_pre
            num_1_pre = num_1_now

            if map[i][j+1]!=0:
                num_2_now = map[i][j+1]
            else:
                while map[i][j+1] == 0 and (j+1)<3:
                    j += 1
                num_2_now = map[i][j+1]
            num_2_pre = num_2_now
            if num_1_now < num_2_now:
                totals[0] += 1
    for j in range(4):
        for i in range(3):
            if map[i][j]!=0:
                num_1_now = map[i][j]
            else:
                num_1_now = num_1_pre
            num_1_pre = num_1_now

            if map[i+1][j]!=0:
                num_2_now = map[i+1][j]
            else:
                while map[i+1][j] == 0 and (i+1)<3:
                    i += 1
                num_2_now = map[i+1][j]
            num_2_pre = num_2_now
            if num_1_now < num_2_now:
                totals[0] += 1

    #decrease
    for i in range(4):
        for j in range(3):
            if map[i][j]!=0:
                num_1_now = map[i][j]
            else:
                num_1_now = num_1_pre
            num_1_pre = num_1_now

            if map[i][j+1]!=0:
                num_2_now = map[i][j+1]
            else:
                while map[i][j+1] == 0 and (j+1)<3:
                    j += 1
                num_2_now = map[i][j+1]
            num_2_pre = num_2_now
            if num_1_now > num_2_now:
                totals[1] += 1
    for j in range(4):
        for i in range(3):
            if map[i][j]!=0:
                num_1_now = map[i][j]
            else:
                num_1_now = num_1_pre
            num_1_pre = num_1_now

            if map[i+1][j]!=0:
                num_2_now = map[i+1][j]
            else:
                while map[i+1][j] == 0 and (i+1)<3:
                    i += 1
                num_2_now = map[i+1][j]
            num_2_pre = num_2_now
            if num_1_now > num_2_now:
                totals[1] += 1
    if totals[0] > totals[1]:
        return totals[0]
    else:
        return totals[1]

'''
