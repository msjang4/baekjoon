import sys
from bisect import bisect_left
try:
    read = open('stdout.txt','r').readline
except:
    read = sys.stdin.readline

n,m = map(int,read().split())
match = [-1]*m
adj =[]

for _ in range(n):
    t, *li = map(int,read().split())
    adj.append(li)

def dfs(a:int):#a에서 매칭될 수 있는 b찾기
    if a in visited: #a를 방문했었다는 건 dfs(a)가 False라는 거임. 따라서, A그룹의 각 정점마다 최대 모든 간선을 한번씩만 탐색하면 되므로 O(VE)임.
        return False
    visited.add(a)
    for b in adj[a]:
        b-=1 # 0 index로 바꿈
        if match[b] == -1 or dfs(match[b]):# b가 매칭된 a가 있다면 증가경로를 찾음. 증가경로는 현재 a에서 매칭된 정점들만 거친 후 매칭되지 않은 b로 가는 경로
            match[b] = a
            return True
    return False



ans=0

for a in range(n):
    visited = set()
    if dfs(a):
        ans+=1

print(ans)
