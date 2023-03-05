import sys
from math import ceil, log2
from bisect import bisect
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

maxy, miny = map(int,read().split())

dy = maxy-miny
n = int(read())


x_li = []
#문제가 특이한게 기울기를 dy/dx가 아니라 dx/dy로 생각해야 함.
for _ in range(n):
    upx,lowx = map(int,read().split())

    x_li.append((lowx-upx,upx))
    #dx는 정렬시 큰 것부터
    # 기울기가 같다면 upx가 큰순으로 정렬

idx = [i for i in range(n)]

idx.sort(lambda idx: x_li[idx],reverse=True)
stk = [idx[0]]

def get_cross_y(a,b):
    dx1, upx1, dx2, upx2 = *x_li[a],*x_li[b]
    if dx1-dx2==0:
        return float('inf')

    #ay+b와 cy+d의 교점의 x의좌표는?
    # (d-b)/(a-c)임 maxy에서 y좌표를 빼면 y교점구할수잇음
    return maxy- (upx2-upx1)*dy/(dx1- dx2)
size=1
for i in range(1,n):
    while True:
        if size == 1:
            stk.append(idx[i])
            size+=1
            break
        else:
            y1 =get_cross_y(stk[-2],stk[-1])
            y2 = get_cross_y(stk[-1],idx[i])
           # print(stk[-2]+1,stk[-1]+1,idx[i]+1,y1,y2)
            if y2 > y1: #upx가 큰순으로 정렬햇으므로 평행한경우 pop시켜야하는데.
                        #평행하면 y2가 inf라 y2>y1이 항상참
                stk.pop()
                size-=1

                continue

            stk.append(idx[i])
            size+=1
            break


def search(y):
    b,e=0,size-1

    while b<e:
        m= (b+e)//2
        if get_cross_y(stk[m],stk[m+1]) <= y:
            e=m
        else:

            b=m+1
    return stk[b]+1
m = int(read())


for _ in range(m):
    y = float(read())
    print(search(y))
