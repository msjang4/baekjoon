import sys
from math import ceil
from bisect import bisect_left
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n = int(read())
m = n


arr = [list(map(int, read().split())) for _ in range(n)]

adj = [[] for _ in range(n)]

for i in range(n):
    for j in range( m):
        cnt=0
        for k in range(3):
            if arr[i][k] < arr[j][k]: #하나라도 스탯이 딸리면 못먹음
                break
            elif arr[i][k] == arr[j][k]:
                cnt+=1
        else:
            if cnt!=3 or i<j: #스탯이 모두 같으면 i<j인경우에만 매칭될수있음
                adj[i].append(j)


def dfs(a):  # a에서 매칭될 수 있는 b찾기

    if a in visited:  # a를 방문했었다는 건 dfs(a)가 False라는 거임. 따라서, A그룹의 각 정점마다 최대 모든 간선을 한번씩만 탐색하면 되므로 O(VE)임.
        return False
    visited.add(a)
    for b in adj[a]:
        if match[b] == -1 or dfs(match[b]):  # b가 매칭된 a가 있다면 증가경로를 찾음. 증가경로는 현재 a에서 매칭된 정점들만 거친 후 매칭되지 않은 b로 가는 경로
            match[b]=a
            return True
    return False


match = [-1]*n
cnt=0
for a in range(n):
    for _ in range(2):
        visited = set()
        if dfs(a):
            cnt += 1

print(n-cnt)