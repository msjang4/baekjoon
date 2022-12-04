import sys
import math
from heapq import heappush, heappop
from collections import deque
from itertools import permutations
from pprint import pprint
from functools import cmp_to_key
from math import atan2
read = sys.stdin.readline


def dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def cccw(p1, p2, p3, p4):
    return (p2[0]-p1[0]) * (p4[1]-p3[1]) - (p4[0]-p3[0]) * (p2[1]-p1[1])
def slope(p1,p2):
    #p1 -> p2 일때 dy/dx
    if p1[0]==p2[0]:
        return float('inf')
    else:
        return (p2[1]-p1[1])/(p2[0]-p1[0])


t = int(read())
for _ in range(t):
    n = int(read())

    arr = [list(map(int, read().split())) for _ in range(n)]

    arr.sort() # x좌표가 작은 순으로 정렬해야 dy/dx 순으로 정렬시 반시계방향으로 정렬됨
    std = arr[0] #기준점

    arr=sorted(arr[1:],key=lambda x: slope(std,x)) # 평행한 경우에는 x가 작은 것부터 scan해야 양끝점이 되나 stable 정렬이므로 명시하지 않아도됨.
    # arr = sorted(arr[1:], key = cmp_to_key(lambda p1,p2: -cccw(std,p1,p1,p2) ))
    # ccw로 정렬하는 방법이있는데 같은 시간복잡도여도 단순 기울기 계산보다 연산이 많이 필요해서 시간초과 난다.

    stk = [std,arr[0]]
    for i in range(1,n-1): #기준점, 두번째 제외 n-2개
        nex = arr[i]
        while len(stk)>=2:
            sec = stk.pop()
            fir = stk[-1] # fir,sec,nex의 ccw값에 상관없이 어차피  fir는 다시 스택에 들어가므로
            #pop하지 않고 top으로 값만 추출

            if cccw(fir,sec,sec,nex)>0: #변에 점이 여러 개 있는 (= 평행한) 경우에는 가장 양 끝 점만 개수에 포함
                stk.append(sec)  #fir, sec,next가 반시계방향이라 sec를 convex hull 요소로 넣는 것.
                break
            # fir,sec,next가 시계방향이면 while문을 한번더 돌게 되고 그때는 fir가 sec가 되고 fir이전게 fir가 됨.
            #근데 stk에 2개 이상없으면 그만둠.
        stk.append(nex)
    ls = len(stk)
    ans = (0, 0, 1)
    b = 1
    for a in range(ls):  # 로테이팅 캘리퍼스 알고리즘
        while  cccw(stk[a], stk[(a + 1) % ls], stk[b % ls], stk[(b + 1) % ls]) > 0: #시계방향 될때까지 b 이동
            b += 1

        d = dist(stk[a], stk[b % ls])
        if ans[0] < d:
            ans = (d, a, b % ls)

    print(*stk[ans[1]], *stk[ans[2]])



