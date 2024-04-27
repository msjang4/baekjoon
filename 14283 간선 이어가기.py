"""input
8 9
1 2 3
1 3 2
1 4 4
2 5 2
3 6 1
4 7 3
5 8 6
6 8 2
7 8 7
1 8
"""
# v^2e = 2500*1000 = 2500000 250만정도 이걸 1000번 반복? 25억?

import sys
read = sys.stdin.readline

N,M = map(int,read().split())

adj = [[] for i in range(N+1)]
edges = []
w_sum = 0
for i in range(M):
    u,v,c = map(int,read().split())
    w_sum+=c
    
    adj[u].append([v,c, len(adj[v])])

    adj[v].append([u,c, len(adj[u])-1])
    edges.append((u, len(adj[u])-1,v, len(adj[v])-1, c))


s, t= map(int,read().split())


from collections import deque



def level_graph(s):

    q = deque([s])
    level[s] = 0

    while q:
        u = q.popleft()
        for v,c,rev in adj[u]:
            if c > 0 and level[v] == -1:
                q.append(v)
                level[v] = level[u]+1
            
        

def dfs(u, t, fin=float('inf')):
    if u==t:
        return fin
    while iter[u] < len(adj[u]):
        v,c, rev = adj[u][iter[u]]
        if c > 0 and level[u] < level[v]:

            if fout:=dfs(v, t, min(fin, c)) > 0:
                adj[u][iter[u]][1] -= fout
                adj[v][rev][1] +=fout
                return fout
        iter[u]+=1
    return 0




def dinic(s,t, fin=float('inf')):
    global level, iter

    flow =0
    while True:
        level =[-1] * (N+1)
        level_graph(s)
        if level[t] == -1 or fin ==0:
            break
        
        iter = [0]*(N+1)
        while f:=dfs(s,t, fin) > 0:
            flow +=f
            fin -= f
    # cut set중에서 최대 가중치를 갖는 간선을 찾아야함.
    return flow

answer = 0
flow = 0
for i in range(M):
    for u,idx,v,rev,c in edges:
        adj[u][idx][1] = c
        adj[v][rev][1] =c

    u,idx,v,rev, _ = edges[i]

    adj[u][idx][1] = 0
    adj[v][rev][1] = 0 

    answer= max(answer,w_sum-dinic(s,t))

print(answer)



        





# print(N,M,s,t)


