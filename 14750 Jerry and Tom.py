import sys
from math import ceil
from bisect import bisect_left
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n, k,h,m = map(int, read().split())

corners = [ list(map(int,read().split())) for _ in range(n)]
holes = [list(map(int,read().split())) for _  in range(h)]
mice = [list(map(int,read().split())) for _ in range(m)]
corners.append(corners[0]) #마지막코너 - 시작코너로 선분을 만들수 있도록

size = m+h+2#쥐수 + 구멍수 + source,sink =총 n+m+2개

adj = [[] for _ in range(size)]
ref = [[] for _ in range(size)]
flow = [[] for _ in range(size)]
cap = [[] for _ in range(size)]
s=0; e=size-1;

def ccw(p1,p2,p3):

    a = p2[0] - p1[0]
    b = p2[1] - p1[1]
    c = p3[0] - p2[0]
    d = p3[1] - p2[1]
    return a*d-b*c

def iscross(p1,p2,p3,p4):
    if ccw(p1,p2,p3)*ccw(p1,p2,p4)==0 and ccw(p3,p4 ,p1)* ccw(p3,p4,p2)==0:
        minp1,maxp1 = sorted([p1,p2])
        minp2,maxp2 = sorted([p3,p4])
        if maxp1[0] <minp2[0] or maxp2[0] < minp1[0]:
            return False
        if minp1[0] == maxp1[0] and minp2[0] == maxp2[0]:
            if maxp1[1] < minp2[1] or maxp2[1] < minp1[1]:
                return False
        return True
    if ccw(p1,p2,p3)*ccw(p1,p2,p4) <=0 and ccw(p3,p4,p1)* ccw(p3,p4,p2)<=0:
        return True
    return False
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


for u,mouse in enumerate(mice,start=1):
    add_edge(s,u)
    for v,hole in enumerate(holes,start=1):
        for l in range(n):
            c1,c2 = corners[l], corners[l+1]
            if iscross(hole,hole,c1,c2): #구멍자체가 c1-c2선분위에 있으면 제외
                continue
            if iscross(mouse,hole,c1,c2): #벽에 가려지면 break

                break
        else: #모든 벽에 가려지지 않았으면

            add_edge(u,v+m)

for v in range(1,h+1):
    add_edge(v+m,e,k) #구멍이 수용할수 있는 쥐수는 k


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
                flow[v][ref[u][i]] -= flux
                return flux

        work[u]+=1 #i번 간선을 이 level 그래프 에서 제외함.
    return 0

ans=0;
while bfs():
    work = [0] * size
    #print(level)
    while flux:=dfs(s,1):
        ans+=1
if ans == m:

    print('Possible')
else:
    print('Impossible')

