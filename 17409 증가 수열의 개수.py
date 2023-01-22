import sys
from math import ceil,log2
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**5)
n,k = map(int,read().split())

arr = [*map(int, read().split())]


size = 2**ceil(log2(100_000+1))

segtrees=[None]+[ [0]*(2*size) for _ in range(10)]
#k번째 segtree는 k길이의 증가수열을 만들때 그 증가수열의 마지막 수가 i인것의 sumtree임
MOD = 10**9+7


def update(i,d,k): #logn
    i= size+i
    while i:
        segtrees[k][i] = (segtrees[k][i]+d)%MOD
        i>>=1

def query(l,r,k,i=1,b=0,e=size-1): #logn
   # print(l,r,k,b,e)
    if r<b or e<l:
        return 0;

    if l<=b and e <= r:
        return segtrees[k][i]
    elif i< size:
        m= (b+e)//2
        if r<=m: #파이썬에서 재귀는 시간을 많이 잡아먹어서 if문을 써서 재귀호출을 반으로 줄인다.
            return query(l,r,k,i*2, b,m)
        elif m<l:
            return query(l,r,k,i*2+1,m+1,e)
        return query(l,r,k,i*2, b,m)+query(l,r,k,i*2+1,m+1,e)
    else:
        return 0;


for x in arr:
    update(x,1,1)
    for i in range(2,k+1): #10*2logn
        update(x,query(0,x-1,i-1)%MOD,i)

print(query(0,100_000,k)%MOD)
