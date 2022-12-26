import sys
from math import ceil
from bisect import bisect_left
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

sys.setrecursionlimit(10**5)

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


t =int(read())

for _ in range(t):
    n,m = map(int,read().split())

    size=n*m+2 #행 수 +열 수 + sink,source, 행에서 열로가는 간선의 flow가 숫자값이고 이 간선의 cap 제한을 이분탐색하면 됨.
    adj = [[] for _ in range(size)]
    ref = [[] for _ in range(size)]
    flow = [[] for _ in range(size)]
    cap = [[] for _ in range(size)]
    s = n*m
    e = n*m+1

    mp = [list(map(int,read().split())) for _ in range(n)]
    dx = [0,0,1,-1]
    dy = [1,-1,0,0]


    for y in range(n):
        for x in range(m):
            if (y+x) %2 : # 좌표쌍이 홀수인경우에만 ,
                #즉 체크판 처럼 정점들을 두그룹(A,B)으로 분리하고 최대유량을 구한다.
                # s->A  남은 용량이랑 B->e 남은 용량은 상하좌우에 양수가 없으므로 용량만큼 연산을 더해줘야함.
                # 즉 최대유량 + 남은용량이 최소횟수다.



                for i in range(4):
                    nx = x+dx[i]
                    ny = y +dy[i]
                    if nx in range(m) and ny in range(n):
                        add_edge(y*m+x, ny*m+nx,float('inf'))
                add_edge(s,y*m+x, mp[y][x])
            else:
                add_edge(y*m+x,e,mp[y][x])

    ans=0
    while bfs():
        work = [0] * size
        while flux:=dfs(s,float('inf')):
            ans+=flux

    # 남은 유량에 대해 한번더 생각해보면 유량을 1흘려줄때마다 격자 내 2개의 숫자가 2감소한거고
    # 유량 f를 흘려줫을때 격자 내 남은 숫자들의 합계는 S- 2*f다.
    # 따라서 f를 최대유량이라고 하면 f + S- 2*f = S-f, 즉 전체합계에서 최대유량을 빼준게 답이다.

     #2차원 배열 합계는 map으로 쉽게 구할 수 있음
    print(sum(map(sum,mp))-ans)

