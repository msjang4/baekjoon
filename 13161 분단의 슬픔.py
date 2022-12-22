import sys
from math import ceil
from bisect import bisect_left
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n= int(read())

ter = list(map(int,read().split())) #진영

mp = [list(map(int,read().split())) for _ in range(n)]




size=n+2 #source, sink, n명 사람 *2
adj = [[] for _ in range(size)]
ref = [[] for _ in range(size)]
flow = [[] for _ in range(size)]
cap = [[] for _ in range(size)]
s=n; e=n+1;
li1=[]
li2=[]
def add_edge(u,v,c=1,bi=False):
    ref_v, ref_u = len(adj[v]),len(adj[u])
    adj[u].append(v)
    flow[u].append(0)
    cap[u].append(c)
    ref[u].append(ref_v)

    adj[v].append(u)
    flow[v].append(0)
    cap[v].append(c if bi else 0)
    ref[v].append(ref_u)

for u in range(n):


    for v in range(u+1,n):
        add_edge(u,v,mp[u][v],True) #양방향간선 추가
    if ter[u] ==1:
        add_edge(s,u,float('inf'))

    elif ter[u]==2:
        add_edge(u,e,float('inf'))


def bfs():
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
    while flux:=dfs(s,float('inf')):
        ans+=flux
print(ans)


bfs()
# s에서 u로 유량이흐른다는 건 u가 B진영이 아니라는 뜻
# B진영이였으면 이미 s->e의 모든경로(슬픈정도)가 포화돼서 흐를 수 없음
# 따라서 visited배열로 진영을 알 수 있다.

for u in range(n):
    if u in visited:
        li1.append(u + 1)
    else:
        li2.append(u+1)

print(*li1)
print(*li2)
