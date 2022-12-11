import sys
from math import ceil
from bisect import bisect_left

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n,k = map(int,read().split())
adj = [[] for _ in range(n+1)]
for i in range(k):
    x,y = map(int, read().split())
    adj[x].append(y)
    #행과 열을 최소로 선택해서 돌멩이를 골라내는 건
    #행과 열을 버텍스로 보고 돌멩이를 간선으로 본 후 최소 버텍스 커버를 구하면된다.
    #즉, 돌멩이의 좌표 (x,y)가 간선 (x,y)이다.

match = [-1]*(n+1)
def dfs(a):

    if a in visited:
        return False
    visited.add(a)
    for b in adj[a]:
        if match[b] == -1 or dfs(match[b]):
            match[b] = a
            return True
    return False

ans=0
for a in range(1,n+1):
    visited = set()
    if dfs(a):
        ans+=1

print(ans)



