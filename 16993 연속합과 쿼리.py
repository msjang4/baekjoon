import sys
from math import ceil,log2
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**3)
n = int(read())

arr = [*map(int, read().split())]

prefix = 0
suffix = 0

size = 2**ceil(log2(n+1))
default = -float('inf')
presum = [0]*n
sufsum = [0]*n
segpre = [0]*(2*size)
segsuf = [0]*(2*size)

for i in range(n):
    prefix+= arr[i]
    suffix+= arr[n-i-1]
    presum[i] = prefix
    sufsum[n-i-1] = suffix

segpre[size+1:size+1+n] = presum
segsuf[size+1:size+1+n] = sufsum

def init_sum(i=1):

    if i< size:
        init_sum(i*2)
        init_sum(i*2+1)
        segpre[i] = max(segpre[i*2],segpre[i*2+1])
        segsuf[i] = max(segsuf[i*2],segsuf[i*2+1])

def query_pre(l,r,i=1,b=0,e=size-1):

    while True:
        if l<=b and e <=r:
            return segpre[i]
        elif i< size:
            m= (b+e)//2
            if r<=m: #l<b<= r<=m 인경우 오른쪽자식은 볼필요없다.
                i,e= i*2,m
            elif m+1<=l: # m+1<=l<= e < r인경우 왼쪽자식은 볼필요없다.
                i,b= i*2+1,m+1
            else:
                return max(query_pre(l,r,i*2,b,m), query_pre(l,r,i*2+1,m+1,e))
        else:
            return default

def query_suf(l,r,i=1,b=0,e=size-1):
    while True:
        if l <= b and e <= r:
            return segsuf[i]
        elif i < size:
            m = (b + e) // 2
            if r <= m:  # l<b<= r<=m 인경우 오른쪽자식은 볼필요없다.
                i, e = i * 2, m
            elif m + 1 <= l:  # m+1<=l<= e < r인경우 왼쪽자식은 볼필요없다.
                i, b = i * 2 + 1, m + 1
            else:
                return max(query_suf(l, r, i * 2, b, m), query_suf(l, r, i * 2 + 1, m + 1, e))
        else:
            return default

init_sum()


segtree = [default]*(2*size)

segtree[size+1:size+1+n] = arr #해당 구간내에 최대 연속합을 segtree로 저장

def init(i=1,b=0,e=size-1):
    if i<size:
        m=(b+e)//2
        init(i*2,b,m)
        init(i*2+1,m+1,e)
        # l,r을 두구간으로 나눴을때 경계선 m,m+1 을 기준으로 m이전거만 포함하는 연속합은 query(l,m), m+1이후거만 포함하는 연속합은 query(m+1,r)로
        # m,m+1을 포함하는 연속합은 greedy하게 구할 수 있다.
        if 1<=b and e <= n:
            query_bm =query_suf(b,m)
            query_me = query_pre(m+1,e)
            segtree[i] = max(segtree[i*2],segtree[i*2+1],query_bm +query_me - sufsum[m] - presum[m-1] )


def query(l,r,i=1,b=0,e=size-1):
    while True:
        if l <= b and e <= r:
            return segtree[i]
        elif i < size:
            m = (b + e) // 2
           # print(b,m,e)
            if r <= m:  # l<b<= r<=m 인경우 오른쪽자식은 볼필요없다.
                i, e = i * 2, m
            elif m + 1 <= l:  # m+1<=l<= e < r인경우 왼쪽자식은 볼필요없다.
                i, b = i * 2 + 1, m + 1
            else: # b<= l <=m , m+1 <=r <=e 인경우 m,m+1을 포함하는 경우를 greedy하게 구해서 비교해야함.
                query_bm =  query_suf(l,m)
                query_me = query_pre(m+1,r)
                return max(query(l,r,i*2,b,m),query(l,r,i*2+1,m+1,e),query_bm +query_me - sufsum[m] - presum[m-1] )
        else:
            return default

init()
m= int(read())
ans = [0]*m
for i in range(m):
    l,r = map(int,read().split())
    ans[i]= str(query(l,r))
print('\n'.join(ans))
