import sys
from math import ceil, log2
from bisect import bisect
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline


n = int(read())


size = 2**ceil(log2(2*n))
segtree = [0]*(2*size)
lazy = [0]*(2*size)
y_li = []
for i in range(n):
    x1,y1,x2,y2 = map(int,read().split())
    y_li.append((y1,y2)) # y좌표들을 수직선위에 있는 선분이라고 생각하고 y_li에 넣되
    y_li.append((y2,y1)) # 선분의시작은 y1<y2고 선분의 끝은 y1>y2가되게 넣는다

def propagate(i):
    if lazy[i]:
        segtree[i]+=lazy[i]
        if i<size:
            lazy[i*2] +=lazy[i]
            lazy[i*2+1]+= lazy[i]

        lazy[i] = 0

def update(l,r,d,i=1,b=0,e=size-1):
    propagate(i)
    if r < b or e < l:
        return

    if l<= b and e <=r:

        segtree[i]+=d
        if i<size:
            lazy[i*2]+=d
            lazy[i*2+1]+=d
    elif i<size:
        m= (b+e)//2
        update(l,r,d,i*2,b,m)
        update(l,r,d,i*2+1,m+1,e)
        segtree[i] = max(segtree[i*2],segtree[i*2+1])

def init(i=1):
    if i<size:
        init(i*2)
        init(i*2+1)
        segtree[i] = max(segtree[i*2],segtree[i*2+1])
y_li.sort(key=lambda x:(x[0],-x[1])) #두번째는 내림차순으로 해야됨
#그래야 선분의 시작 부터 뽑을 수 있음.

y_idx = {
}

rank=-1
prev_y = -float('inf'),-float('inf')
cnt=0
arr = [0]*(2*n)
for y1,y2 in y_li:
    if  prev_y[0] < prev_y[1] and (y1 > y2 or  y1 !=prev_y[0]):
        # 이전 y가 선분의 시작인 경우
        # 이전 y랑 지금 y랑 다르거나 지금 y가 선분의끝이라면
        # cnt를 업뎃해줘야함.
        arr[rank] =cnt #압축된 좌표별로 사각형개수
    if prev_y[0]!=y1:
        rank+=1
        y_idx[y1] = rank
        arr[rank] =cnt
    if y1< y2:
        cnt +=1
    else:
        cnt -=1
    prev_y = y1,y2
segtree[size:size+2*n] = arr
init()
ans= 0
prev_y =  -float('inf'),-float('inf')
for y1,y2 in y_li:
    if  prev_y[0] < prev_y[1] and (y1 > y2 or  y1 !=prev_y[0]):
        #이전 y가 선분의 시작인 경우
        #이전 y랑 지금 y랑 다르거나 지금 y가 선분의끝이라면
        # ans를 업뎃해줘야함.
        ans=max(ans, segtree[1]+arr[y_idx[prev_y[0]]])
    if y1 < y2:
        update(y_idx[y1],y_idx[y2],-1) #선분의 시작이니까 이 선분의 끝을 만날때까지
        #[y1,y2]구간에 1을 빼놔야 교차하는 사각형개수를 중복되지 않게 셀수 있음.
    else:
        update(y_idx[y2],y_idx[y1],+1)
    prev_y = y1,y2
print(ans)
