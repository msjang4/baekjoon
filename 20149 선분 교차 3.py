'''input
2 8 9 23
1 10 9 8
'''
import sys
from heapq import heappush, heappop
from collections import deque
from pprint import pprint
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10 ** 5)
# n= int(read())


arr = list(map(int, read().split())) + list(map(int, read().split()))


def getS(a, b, c):
    x1, y1 = arr[a * 2], arr[a * 2 + 1]
    x2, y2 = arr[b * 2], arr[b * 2 + 1]
    x3, y3 = arr[c * 2], arr[c * 2 + 1]
    # print(x2,y2, x3,y3)
    return 0.5 * (x1 * y2 + x2 * y3 + x3 * y1 - (x2 * y1 + x3 * y2 + x1 * y3))


def check():
    if getS(0, 1, 2) == 0 and getS(0, 1, 3) == 0: #평행한경우 영벡터일수없어서 getS(2,3,0) , getS(2,3,1)은 확인안해도됨

        min12x = min(x1, x2)
        max12x = max(x1, x2)
        min12y = min(y1, y2)
        max12y = max(y1, y2)

        min34x = min(x3, x4)
        max34x = max(x3, x4)
        min34y = min(y3, y4)
        max34y = max(y3, y4)

        if max34x < min12x or max12x < min34x or max34y < min12y or max12y < min34y: # 이경우들은 절대로 만날수없음.
            return 0
        elif max34x == min12x: # max x랑 minx가 겹치면 한점에서 반드시 만나는거다.
            print(1)
            if max34y==min12y:

                print(max34x, max34y )
            elif min34y == max12y:
                # x좌표 4개가 한점에서 겹친다면
                # max34y!= min12y라고해서 min34y = max12y가 아니므로 if로 확인해야함. 즉, 43번 줄 주석의 가정은 틀린거임.
                print(max34x, min34y)
            exit(0)
        elif max12x == min34x:
            print(1)
            print(max12x, max34y if max34y == min12y else min34y)
            exit(0)
        else: #한점에서 만나지 않고 선분자체가 겹침.
            return 2

    if getS(0, 1, 2) * getS(0, 1, 3) <= 0 and getS(2, 3, 0) * getS(2, 3, 1) <= 0:
        return 1
    else:
        return 0


x1, y1 = arr[0], arr[1]
x2, y2 = arr[2], arr[3]
x3, y3 = arr[4], arr[5]
x4, y4 = arr[6], arr[7]
res = check()
if res == 2:
    print(1)
elif res:
    print(1)
    if x1 == x2:
        m2 = (y4 - y3) / (x4 - x3)
        print(x1, m2 * (x1 - x3) + y3)
        exit(0)
    elif x3 == x4:
        m1 = (y2 - y1) / (x2 - x1)
        print(x3, m1 * (x3 - x1) + y1)
        exit(0)

    m1 = (y2 - y1) / (x2 - x1)
    # print('{}(x -{})+{}'.format(m1,x1,y1))
    m2 = (y4 - y3) / (x4 - x3)
    # print('{}(x -{})+{}'.format(m2,x3,y3))

    xx = (y3 - y1 + m1 * x1 - m2 * x3) / (m1 - m2)
    yy = m1 * (xx - x1) + y1
    print(xx, yy)
else:
    print(0)







