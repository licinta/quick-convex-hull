import cmath
import heapq
from sys import setrecursionlimit

import matplotlib.pyplot as plt

setrecursionlimit(10005)


def toPolar(p1, p2):
    p = [p2[0] - p1[0], p2[1] - p1[1]]
    l, sita = cmath.polar(complex(*p))
    return sita


def drawPoxy(linepoints):
    if not linepoints:
        return
    linepoints.sort(key=lambda x: x[0])
    stack = [linepoints[0]]
    heap = [linepoints[1:]]
    heapq.heapify([(-toPolar(linepoints[0], i), i) for i in linepoints[1:]])
    while heap:
        stack.append(heapq.heappop(heap)[1])

    stack.append(stack[0])
    for i in range(len(stack) - 1):
        plt.plot([stack[i][0], stack[i + 1][0]], [stack[i][1], stack[i + 1][1]])


def drawPanel(points: list[list], linepoints=()):
    for i, j in points:
        plt.scatter(i, j, )
    if linepoints:
        linepoints.sort(key=lambda x: x[0])
        stack = [linepoints[0]]
        heap = linepoints[1:]
        heap = [(-toPolar(linepoints[0], i), i) for i in heap]
        heapq.heapify(heap)
        while heap:
            stack.append(heapq.heappop(heap)[1])
        stack.append(stack[0])
        plt.plot([i[0] for i in stack], [i[1] for i in stack])

    plt.show()


def generatePoints(n):
    from random import randint
    points = []
    for i in range(n):
        points.append(tuple([randint(-1000000, 1000000), randint(-1000000, 1000000)]))
    return points


k_inf = 0x7fffffff


def getline(p1, p2):
    # y=k(x-a)+b
    if p1[0] == p2[0]:
        return [k_inf, p1[0], 0]
    if p1[1] == p2[1]:
        return [0, 0, p1[1]]
    k = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p1[1] - k * p1[0]
    return [k, 0, b]


def dis(p, l, r):
    k, a, b = getline(l, r)
    return (k * p[0] - p[1] - k * a + b) / (1 + k ** 2) ** 0.5


def split(points, l, r):
    pdown, pdown_d, pup, pup_d = [], 0, [], 0
    p1, p2 = None, None
    for i in points:
        if i == l or i == r:
            continue
        d = dis(i, l, r)
        if d < 0:
            pdown.append(i)
            if abs(d) > pdown_d:
                pdown_d = abs(d)
                p1 = i
        if d > 0:
            pup.append(i)
            if abs(d) > pup_d:
                pup_d = abs(d)
                p2 = i
    # print(pdown, pup, p1, p2, sep='\n')
    return pdown, pup, p1, p2


def find(points, l, r, direction, ans):
    pd, pu, p1, p2 = split(points, l, r)
    if direction:
        if pu:
            ans.add(p2)
            find(pu, l, p2, direction, ans)
            find(pu, p2, r, direction, ans)
        else:
            return
    else:
        if pd:
            ans.add(p1)
            find(pd, l, p1, direction, ans)
            find(pd, p1, r, direction, ans)
        else:
            return


def getTB(points):
    points.sort(key=lambda x: x[0])
    l, r = points[0], points[-1]
    tb = set([l, r])
    up = True
    down = False
    pd, pu, p1, p2 = split(points, l, r)
    tb.add(p1)
    tb.add(p2)
    find(pu, l, p2, up, tb)
    find(pu, p2, r, up, tb)
    find(pd, l, p1, down, tb)
    find(pd, p1, r, down, tb)
    return list(tb)


points = generatePoints(100)
tb_points = getTB(points)
print(tb_points)
drawPanel(points, tb_points)
