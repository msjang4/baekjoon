import sys
from math import ceil,log2
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**3)
n = int(read())

arr = [*map(int, read().split())]


size = 2**ceil(log2(n+1))

segtree = [0]*(2*size)

presum = [0]*(size)
s=0
for i in range(n):
    s+=arr[i]
    presum[i+1]=s
    segtree[size+1+i] = (arr[i],arr[i],arr[i])
    #b~e구간 segtree의 요소는 3가지다
    # 1. b번째 수를 가장 처음으로 하는 연속합의 최댓값 = lmax
    # 2. e번째 수를 가장 마지막으로 하는 연속합의 최댓값 = rmax
    # 3. b~e구간의 연속합 중 최댓값 =mmax
    # 이렇게 하면 상위구간의 각 요소는 다음과 같이 구할 수 있다.
    # 1. 왼쪽자식 구간합 + 오른쪽자식 lmax
    # 2. 오른쪽자식 구간합 + 왼쪽자식 rmax
    # 3. 왼쪽자식 mmax, 오른쪽 자식 mmax, 왼쪽자식 rmax +오른쪽자식 lmax 중 최댓값

    
def init(i=1,b=0,e=size-1):

    if i< size:
        m= (b+e)//2
        init(i*2,b,m)
        init(i*2+1,m+1,e)
        if 1<=b and e <=n:
            lsum = presum[m]-presum[b-1]
            rsum = presum[e]-presum[m]
            lmax = max(segtree[i*2][0], lsum+segtree[i*2+1][0])
            rmax = max(segtree[i*2+1][1], rsum+segtree[i*2][1])
            mmax = max(segtree[i*2][2],segtree[i*2+1][2], segtree[i*2][1]+segtree[i*2+1][0])
            segtree[i] = (  lmax,rmax, mmax)
init()

def query(l,r,i=1,b=0,e=size-1):
    if r <b or e <l:
        return

    if l<=b and e <=r:
        return segtree[i]
    elif i<size:
        m= (b+e)//2
        if r<=m:
            return query(l,r,i*2,b,m)
        if m+1<=l:
            return query(l,r,i*2+1,m+1,e)
        left = query(l,r,i*2,b,m)
        right = query(l,r,i*2+1,m+1,e)
        lsum = presum[m] - presum[b - 1]
        rsum = presum[e] - presum[m]
        lmax = max(left[0], lsum + right[0])
        rmax = max(right[1], rsum + left[1])
        mmax = max(left[2], right[2], left[1] + right[0])
        return (lmax,rmax,mmax)

m= int(read())
for _ in range(m):
    l,r = map(int,read().split())
    print(query(l,r)[2])