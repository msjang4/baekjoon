import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**5)
n = int(read())

from math import log2, ceil
size= 2**(ceil(log2(n)))
adj = [[] for  i in range(n+1)]

for u, boss in enumerate(map(int, read().split()[1:]),start=2): #1번 제외하고 2번부터
    adj[boss].append(u)

#mmu 1장 더

def euler_tour(u): #오일러투어테크닉을 통해 각 노드들의 자식을 일련된 구간으로 바꿀 수 있다.
    global idx
    euler[u] = idx #u번 노드가 트리전체에서 몇번째로 방문됐는지

    idx+=1
    for v in adj[u]:
        euler_tour(v)
    childs[u]=idx-1 # 마지막 자식노드의 인덱스
def propagate(i,b,e):

    if lazy[i]:
        segtree[i] = (lazy[i]-1)*(e-b+1) #lazy가 2면 1곱하고 1이면 0곱함
        if i < size:
            lazy[i*2] = lazy[i]
            lazy[i*2+1] = lazy[i]
        lazy[i] = 0

def init(i=1):
    
    if i < size:
        init(i*2)
        init(i*2+1)
        segtree[i] = segtree[i*2]+segtree[i*2+1]
    elif i-size < n: #리프노드는 1
        segtree[i] = 1

def update(l,r,d,i=1, b=0,e=size-1): #[l,r]구간을 d만큼 업뎃시킴 , b,e는 현재 노드 i가 관리하는 구간임

    propagate(i,b,e)
    if r<b or e < l :#[b,e]구간과 [l,r]구간이 전혀 겹치지 않는경우
        return
    if l<=b and e <= r: #[b,e]구간이 [l,r]구간에 완전속하는 경우

        segtree[i] = d*(e-b+1)

        if i< size: #리프 아닌경우
            lazy[i*2] =d+1 #0이면 1
            lazy[i*2+1]=d+1 #1이면 2로

    elif i<size: #리프아닌경우
        m= (b+e)//2
        update(l,r,d,i*2,b,m)
        update(l,r,d,i*2+1,m+1,e)
        segtree[i] = segtree[i*2]+segtree[i*2+1]

def query(l,r,i=1,b=0,e=size-1):
    propagate(i, b, e)
    if r < b or e < l:  # [b,e]구간과 [l,r]구간이 전혀 겹치지 않는경우
        return 0
    if l <= b and e <= r:  # [b,e]구간이 [l,r]구간에 완전속하는 경우
        return segtree[i]
    elif i<size: #리프아닌경우
        m = (b + e) // 2
        return query( l, r, i * 2,b, m)+query( l, r, i * 2 + 1,m + 1, e)
    return 0
m=int(read())
euler = [0]*(n+1) #i번 노드가 오일러투어에서 몇번째로 방문한 노드인지
idx =0
childs= [0]*(n+1)# i번 직원의 직속부하중 마지막 부하의 인덱스
euler_tour(1)
segtree = [0]*(2*size) # 이렇게 선언하면 인덱스가 size이상이면 리프노드임.
lazy = [0]*(2*size)
init()

for _ in range(m):
    fc, i = map(int, read().split())
    if fc ==1:#컴퓨터킨다
        update(euler[i]+1,childs[i],1)
    elif fc == 2:#끈다
        update(euler[i]+1,childs[i],0)
    elif fc ==3:
        ans=query(euler[i]+1,childs[i])
        print(ans)

