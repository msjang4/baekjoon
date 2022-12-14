import sys
from math import ceil
from bisect import bisect_left
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n, p = map(int, read().split())
size=2*n+1
adj = [[] for _ in range(size)]
ref = [[] for _ in range(size)]
flow = [[] for _ in range(size)]
cap = [[] for _ in range(size)]
s=1+n; e=2;

def add_edge(u,v):
    ref_v, ref_u = len(adj[v]),len(adj[u])
    adj[u].append(v)
    flow[u].append(0)
    cap[u].append(1)
    ref[u].append(ref_v)

    adj[v].append(u)
    flow[v].append(0)
    cap[v].append(0)
    ref[v].append(ref_u)

#정점을 용량이 1인 간선으로 바꿔서 최대유량을 구하면
# 정점을 한번씩만 거치는 경로의 개수를 구하는 것과 같다.
for _ in range(p):
    u,v = map(int,read().split())

    add_edge(u+n,v) # n이하는 들어오는 정점
    add_edge(v+n,u) #n초과는 나가는 정점

for v in range(1,n+1):
    add_edge(v,v+n) #들어오는 정점과 나가는 정점 사이의 간선 == 원래 정점 개념


def bfs():
    global level
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


def dfs(u,maxflow):
    if u==e:
        return maxflow
    for i in range(work[u],len(adj[u])):
        v = adj[u][i]
        if level[u]+1 ==level[v] and cap[u][i]-flow[u][i] > 0:
            flux = dfs(v,min(maxflow,cap[u][i]-flow[u][i]))
            if flux >0:
                flow[u][i] +=flux
                flow[v][ref[u][i]]-=flux
                return flux

        work[u]+=1 #i번 간선을 이 level 그래프 에서 제외함.
    return 0

ans=0;
while bfs():
    work = [0] * size
    while flux:=dfs(s,1):
        ans+=1

print(ans)