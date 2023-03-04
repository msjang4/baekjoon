import sys
from math import ceil, log2
from bisect import bisect
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10 ** 2)
n = int(read())
x_li= [0]*n
y_li= [0]*n
w_li = [0]*n

idx = [ i for i in range(n)]

for i in range(n):
    x,y,w, = map(int,read().split())
    x_li[i],y_li[i],w_li[i] = x,y,w

idx.sort(key = lambda x: (y_li[x],x_li[x]))
sorted_xli = sorted(x_li)
sorted_yli = sorted(y_li)

size = 2**ceil(log2(n))
def update(x,d,b=0,e=size-1):
    global ans

    i= size+x

    v=segtree[i][0]+d
    segtree[i] = (v,v,v,v)

    i >>= 1
    while i:
        lc = segtree[i * 2]
        rc = segtree[i * 2 + 1]
        lmax = max(lc[3] + rc[0], lc[0])
        rmax = max(rc[3] + lc[1], rc[1])
        mmax = max(lc[2], rc[2], lc[1] + rc[0])

        _sum = lc[3] + rc[3]
        segtree[i] = (lmax, rmax, mmax, _sum)
        i>>=1

adj = [[] for _ in range(n)]
for i in range(n):
    x, y, w = bisect(sorted_xli, x_li[i]), bisect(sorted_yli, y_li[i]), w_li[i]
    adj[y-1].append((x-1,w))

ans=0
for i in range(n):
    segtree = [(0,0,0,0)]*(2*size)

    for j in range(i,n):
        for x,w in adj[j]:
            update(x,w)

        ans= max(ans,segtree[1][2])

print(ans)
