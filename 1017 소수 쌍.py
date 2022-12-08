import sys
from math import ceil
from bisect import bisect_left

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n = int(read())
m = n
arr = list(map(int, read().split()))

p = [True] * (2000 + 1)
p[1] = False  # 1은 소수도 합성수도 아님.
for i in range(2, ceil(2000 ** 0.5)):
    if p[i]:
        for j in range(i * 2, 2000 + 1, i):
            p[j] = False

adj = [[] for _ in range(n)]

for i in range(n):
    for j in range( m):
        if i!=j and p[arr[i] + arr[j]]: #1+1도 소수라 i!=j 안하면 (1,1)을 1쌍이라고 봄
            adj[i].append(j)


def dfs(a: int,x):  # a에서 매칭될 수 있는 b찾기
    if a==x or a==0: #0과 x가 고정매칭이라 0과 x의 증가경로는 False반환
        return False
    if a in visited:  # a를 방문했었다는 건 dfs(a)가 False라는 거임. 따라서, A그룹의 각 정점마다 최대 모든 간선을 한번씩만 탐색하면 되므로 O(VE)임.
        return False
    visited.add(a)

    for b in adj[a]:
        if match[b] == -1 or dfs(match[b],x):  # b가 매칭된 a가 있다면 증가경로를 찾음. 증가경로는 현재 a에서 매칭된 정점들만 거친 후 매칭되지 않은 b로 가는 경로
            match[b] = a
            match[a] = b
            return True
    return False


ans = []
for x in adj[0]: #0과 소수가 될 수 있는 수들에 대해
    match = [-1] * m
    match[0],match[x]=x, 0 #0과 x를 매칭 시켜줌.
    cnt = 1
    for a in range(n):
        if match[a] == -1:  # 쌍이 생기지 않은 수라면
            visited = set()
            if dfs(a,x):
                cnt += 1
    if cnt == n // 2:  # 전체쌍이 생겻다면
        ans.append(arr[x])

if ans:
    ans.sort()  # 오름차순 출력
    print(' '.join(map(str, ans)))
else:
    print(-1)
