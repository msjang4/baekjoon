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
n,m = map(int,read().split())
size=n*m+2 #정점수 + sink,source
mp = [read().strip() for _ in range(n)]
s = n*m
e = n*m+1
adj = [[] for _ in range(size)]
flow = [[] for _ in range(size)]
ref= [[] for _ in range(size)]
cap = [[] for _ in range(size)]
dx = [0,0,1,-1]
dy = [1,-1,0,0]

score = [
[10,8,7,5,1],
[8,6,4,3,1],
[7,4,3,2,1],
[5,3,2,2,1],
[1,1,1,1,0]
]

def get_score(x1,y1,x2,y2): #두 칸의 두부 가격을 구하는 함수
	a=ord(mp[y1][x1])-ord('A')
	b= ord(mp[y2][x2])-ord('A')
	if a>4:
		a=4
	if b>4:
		b=4
	return score[a][b]

for y in range(n):
    for x in range(m):
        if (y+x)%2:
            for i in range(4): #2x1의 점수를 간선의 역비용으로 주고, 용량을 1로 함.
                nx = x+dx[i]
                ny = y+dy[i]
                if nx in range(m) and ny in range(n):
                    add_edge(y*m+x,ny*m+nx,c=1,w=-get_score(x,y,nx,ny)) #비용을 음수로 줘서 최소비용으로 찾을수있게함.

            add_edge(s,y*m+x)

        add_edge(y*m+x,e) #홀수든 짝수든 e로가는 c=1, w=0인간선을 추가함. 홀수인경우는 해당 두부칸을 버리는 것


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
print(-ans)
