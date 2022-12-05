import sys
import math
from heapq import heappush, heappop
from collections import deque
from itertools import permutations
from pprint import pprint
from functools import cmp_to_key
from math import pi
debug = True
if debug:
    read = open('stdout.txt','r').readline
else:
    read = sys.stdin.readline

def dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)**0.5


def cccw(p1, p2, p3, p4):
    return (p2[0]-p1[0]) * (p4[1]-p3[1]) - (p4[0]-p3[0]) * (p2[1]-p1[1])
def iscross(p1,p2,p3,p4):
    if cccw(p1,p2,p2,p3) ==0 and cccw(p1,p2,p2,p4) ==0 and cccw(p3,p4,p4,p1) ==0 and cccw(p3,p4,p4,p2) ==0:#평행한경우
        #p1,p2가 같은 영벡터가 잇을수있으므로 p3,p4에 대해 p1,p2도 검증해야함.
        minp1, maxp1 = sorted([p1,p2])
        minp2, maxp2 = sorted([p3, p4])
        if maxp2[0] < minp1[0] or maxp1[0] < minp2[0]:
            return False
        if minp1[0] == maxp1[0] and minp2[0] == maxp2[0] :
            #p1,p2가 같은 영벡터일수있으므로 다른벡터도 검증필요. 서로다른 영벡터면 return False됨. 예시: 3,3 / 3,3 / 4,2 / 2,4
            if maxp2[1] < minp1[1] or maxp1[1] < minp2[1]:
                return False
        return True
    return cccw(p1,p2,p2,p3)* cccw(p1,p2,p2,p4)<=0 and  cccw(p3,p4,p4,p1) *cccw(p3,p4,p4,p2) <=0


def slope(p1,p2):
    #p1 -> p2 일때 dy/dx
    if p1[0]==p2[0]:
        return float('inf')
    else:
        return (p2[1]-p1[1])/(p2[0]-p1[0])




def convex(arr):
    n=len(arr)
    arr.sort()  # x좌표가 작은 순으로 정렬해야 dy/dx 순으로 정렬시 반시계방향으로 정렬됨
    std = arr[0]  # 기준점

    arr = sorted(arr[1:],
                 key=lambda x: slope(std, x))  # 평행한 경우에는 y가 큰 것부터 scan해야 양끝점이 됨. (ccw는 평행하더라도 거리가 멀면 ccw값이 더큼)
    # arr = sorted(arr[1:], key = cmp_to_key(lambda p1,p2: -cccw(std,p1,p1,p2) ))
    # ccw로 정렬하는 방법이있는데 같은 시간복잡도여도 단순 기울기 계산보다 연산이 많이 필요해서 시간초과 난다.
   # print('arr:',arr)
    if n == 1:
        return [std]
    stk = [std, arr[0]]
    for i in range(1, n - 1):  # 기준점, 두번째 제외 n-2개
        nex = arr[i]
        while len(stk) >= 2:
            sec = stk.pop()
            fir = stk[-1]  # fir,sec,nex의 ccw값에 상관없이 어차피  fir는 다시 스택에 들어가므로
            # pop하지 않고 top으로 값만 추출

            if cccw(fir, sec, sec, nex) > 0:  # 변에 점이 여러 개 있는 (= 평행한) 경우에는 가장 양 끝 점만 개수에 포함
                stk.append(sec)  # fir, sec,next가 반시계방향이라 sec를 convex hull 요소로 넣는 것.
                break
            # fir,sec,next가 시계방향이면 while문을 한번더 돌게 되고 그때는 fir가 sec가 되고 fir이전게 fir가 됨.
            # 근데 stk에 2개 이상없으면 그만둠.
        stk.append(nex)
    return stk
t = int(read())
for _ in range(t):
    n,m = map(int,read().split())

    arrb = [list(map(int, read().split())) for _ in range(n)]
    arrw = [list(map(int, read().split())) for _ in range(m)]

    cvxb = convex(arrb)
    cvxw = convex(arrw)
    res = 'YES'

    std = cvxw[0]
    if len(cvxb) > 1:
        sign = cccw(cvxb[0],cvxb[1], cvxb[1],std)
        for i in range(1,len(cvxb)):
            if sign*cccw(cvxb[i],cvxb[(i+1)%len(cvxb)],cvxb[(i+1)%len(cvxb)],std) <= 0:
                #std에 대한 ccw 부호가 하나라도 다른경우
                break
        else:
            res = 'NO'

    std = cvxb[0]
    if len(cvxw) > 1:
        sign = cccw(cvxw[0], cvxw[1], cvxw[1], std)
        for i in range(1, len(cvxw)):
            if sign * cccw(cvxw[i], cvxw[(i + 1) % len(cvxw)], cvxw[(i + 1) % len(cvxw)], std) <= 0:
                # std에 대한 ccw 부호가 하나라도 다른 경우

                break
        else:
            res= 'NO'

    for i in range(len(cvxb)):
        for j in range(len(cvxw)):
            if iscross(cvxb[i],cvxb[(i+1)%len(cvxb)], cvxw[j],cvxw[(j+1)%len(cvxw)]):
                res = 'NO'
    print(res)





