import sys
from math import ceil
from bisect import bisect_left
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n, m, k = map(int, read().split())


adj = [[] for _ in range(n+m+2)] #직원수 + 일수 + source,sink =총 n+m+2개
ref = [[] for _ in range(n+m+2)]
flow = [[] for _ in range(n+m+2)]
cap = [[] for _ in range(n+m+2)]
def add_edge(u,v,c=1):
    ref_v, ref_u = len(adj[v]), len(adj[u])
    adj[u].append(v)
    cap[u].append(c)
    flow[u].append(0)
    ref[u].append(ref_v)

    adj[v].append(u)  # 역간선도 추가
    cap[v].append(0)
    flow[v].append(0)
    ref[v].append(ref_u)

for u in range(1,n+1):
    arr=list(map(int,read().split()))
    add_edge(0,u) #source와 u의 간선 , 최대 k+1의 유량을 가질 수 잇음.
    for v in arr[1:]:
        add_edge(u,v+n)

for v in range(1,m+1):
    add_edge(v + n, n + m + 1)  # v와 sink의 간선
def bfs():
    global level
    level = [-1]*(n+m+2)
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
                flow[v][ref[u][i]] -= flux
                return flux

        work[u]+=1 #i번 간선을 이 level 그래프 에서 제외함.
    return 0

#벌점의 합이 k보다 넘어 가면 안됨. 그런데, 처음부터 n+k만큼 흐르게 한다면
#두 사람의 벌점의 합이 k보다 커질 수 있음.
#즉 처음 알고리즘 돌릴때는 source ->직원이 용량이 1이고 두번째 돌릴때 용량을 k+1로 해줘야함.
ans=0;
s=0; e=n+m+1;
while bfs():
    work = [0] * (n +m+ 2)
    #print(level)
    while flux:=dfs(s,1):
        ans+=1
cap[0] = [k+1]*n #두번째 돌릴때는 용량을 k더 늘려서 추가로 flow시켜줌.

cnt=0
while bfs():
    work = [0] * (n +m+ 2)
    while flux := dfs(s,1):
        cnt+=1
        ans+=1
        if cnt==k: #k번 이상은 흘려보낼 수 없음.
            print(ans)
            quit()


print(ans)

