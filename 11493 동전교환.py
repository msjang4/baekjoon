import sys
from math import ceil
from bisect import bisect_left
from collections import deque
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

sys.setrecursionlimit(10**5)

def add_edge(u,v,w=0,c=1):
    ref_u, ref_v = len(adj[u]), len(adj[v])
    adj[u].append((v,w))
    flow[u].append(0)
    cap[u].append(c)
    ref[u].append(ref_v)

    adj[v].append((u,-w)) #역간선은 역비용을 가진다
    flow[v].append(0)
    cap[v].append(0)
    ref[v].append(ref_u)



def spfa():
    q=deque([s])
    dist[s] = 0
    while q:
        u = q.popleft()
        inq[u] = False
        for i,(v,w) in enumerate( adj[u]):

            if cap[u][i] - flow[u][i] > 0  and dist[u]+w < dist[v]: #용량 남아있어야함.
                dist[v] = dist[u]+w
                m[v] = (u,i) #memoization , 인접리스트라서 인덱스도 저장해야함.
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
def backtrack():
    v=e
    flux = float('inf')
    while v!=s: # 최단경로상 흐를 수 있는 최대 유량을 구함
        u,i = m[v]
        flux = min(flux,cap[u][i]-flow[u][i])
        v = u

    v = e
    while v!=s: #구한 유량을 흘려줌.
        u,i = m[v]
        flow[u][i]+=flux
        flow[v][ref[u][i]]-=flux
        v=u

    return flux #최단경로내 최대유랑 리턴
t= int(read())
for _ in range(t):
    n,m = map(int,read().split())
    size=n+2 #정점수 + sink,source

    s = 0
    e = n+1
    adj = [[] for _ in range(size)]
    flow = [[] for _ in range(size)]
    ref= [[] for _ in range(size)]
    cap = [[] for _ in range(size)]

    for _ in range(m):
        u,v = map(int,read().split()) #양방향 간선 생성
        add_edge(u,v,w=1, c=float('inf'))
        add_edge(v,u,w=1, c=float('inf'))


    #vertex color
    vertex_colors = list(map(int,read().split()))
    #coin_color
    coin_colors = list(map(int,read().split()))

    for i in range(n):
        if vertex_colors[i] != coin_colors[i]: #두 색깔중 하나만 검은색인경우만
            v=i+1
            if vertex_colors[i]:#정점이 검은색인경우 sink랑 연결
                add_edge(v, e, c=1)
            else: #동전이 검은색인곳은 source랑 연결
                add_edge(s, v, c=1)

    cnt=0
    ans=0
    while True:
        dist = [float('inf')] * size #거리 = 비용
        inq = [False] * size
        m = [-1] * size
        spfa()
        if dist[e] == float('inf'): #e에 도달할수 없으면 종료
            break
        ans+=dist[e]*backtrack() #비용 * 유량만큼 증가
        cnt+=1
    print(ans)
