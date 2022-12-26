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

def add_edge(u,v,w=0):
    ref_u, ref_v = len(adj[u]), len(adj[v])
    adj[u].append((v,-w)) #비용의 최댓값을 구해야하므로 -1을 곱해서 넣어준다.
    flow[u].append(0)
    cap[u].append(1)
    ref[u].append(ref_v)

    adj[v].append((u,w)) #역간선은 역비용을 가진다
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
size=n+m+2 #사람수 +일 수 + sink,source

s = 0
e = n+m+1
adj = [[] for _ in range(size)]
flow = [[] for _ in range(size)]
ref= [[] for _ in range(size)]
cap = [[] for _ in range(size)]

for u in range(1,n+1):
    arr = list(map(int,read().split()[1:]))
    for i in range(0,len(arr),2):
        add_edge(u,n+arr[i],arr[i+1])
    add_edge(s,u)

for v in range(1,m+1):
    add_edge(n+v, e)
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
print(cnt)
print(-ans)
