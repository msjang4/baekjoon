import sys
from math import ceil
from bisect import bisect_left
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

sys.setrecursionlimit(10**5)

n = int(read())


rows= list(map(int,read().split()))
cols = list(map(int,read().split()))


size=2*n+2 #행 수 +열 수 + sink,source, 행에서 열로가는 간선의 flow가 숫자값이고 이 간선의 cap 제한을 이분탐색하면 됨.
adj = [[] for _ in range(size)]
ref = [[] for _ in range(size)]
flow = [[] for _ in range(size)]
cap = [[] for _ in range(size)]
sum = sum(rows)
s = 2*n
e = 2*n+1
def add_edge(u,v,c=1):
    ref_v, ref_u = len(adj[v]),len(adj[u])
    adj[u].append(v)
    flow[u].append(0)
    cap[u].append(c)
    ref[u].append(ref_v)

    adj[v].append(u)
    flow[v].append(0)
    cap[v].append(0)
    ref[v].append(ref_u)

for y in range(n):

    for x in range(n): #행에서 열로가는 간선
        add_edge(y,n+x, float('inf')) #이 간선 용량을 변경시킬거임.

    add_edge(s,y,rows[y]) #source에서 y번째 행
        #모든 행은 n+1개의 간선을 가지고 있고 마지막간선은 source랑 연결됨

    add_edge(n+y, e, cols[y]) #y번째열에서  sink로

#250 * 500*10000 500만정도?

def bfs(): #level 그래프로 바꿈
    global level,visited
    level = [-1]*size
    q =deque([(s,0)])
    visited = {s}
    while q:
        u,d = q.popleft()
        level[u] = d
        for i,v in enumerate(adj[u]):
            if v not in visited and cap[u][i]-flow[u][i]>0:
                q.append((v,d+1))
                visited.add(v)
    return level[e]!=-1


def dfs(u,maxflow,limit):
    if u==e:
        return maxflow
    for i in range(work[u],len(adj[u])):
        v = adj[u][i]
        if level[u]+1 ==level[v] and cap[u][i]-flow[u][i] > 0:
            flux = dfs(v,min(maxflow,cap[u][i]-flow[u][i]),limit)
            if flux >0:
                flow[u][i] +=flux
                flow[v][ref[u][i]]-=flux
                return flux

        work[u]+=1 #i번 간선을 이 level 그래프 에서 제외함.
    return 0

l = 0
r= 10000+1
while l<=r: #Parameteric Search
    m = (l+r)//2
    limit = m
    ans=0;
    flow = [[0]*len(l) for l in flow] #2차원배열 초기화방법

    for y in range(n) :
        for x in range(n):
            cap[y][x] = limit

    while bfs():
        work = [0] * size
        while flux:=dfs(s,float('inf'),limit):
            ans+=flux

    if ans == sum:
        if l==r: #최적의 제한값
            break
        else: #[l,m]구간에 최적의 제한값이 있음.
            r=m
    else: #limit를 올려야함
        l= m+1


print(limit)
for y in range(n):
    for x in range(n):
        print(flow[y][x], end = ' ')
    print()

