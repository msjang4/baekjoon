#출처 https://glanceyes.tistory.com/entry/BOJ-%EB%B0%B1%EC%A4%80-1648%EB%B2%88-%EA%B2%A9%EC%9E%90%ED%8C%90-%EC%B1%84%EC%9A%B0%EA%B8%B0

'''input
14 14
'''
import sys
from pprint import pprint
read = sys.stdin.readline
sys.setrecursionlimit(10**5) #dfs 최대 깊이 2^14 = 16384
n,m = map(int, read().split())

size = 2**m
dp = [[-1]*size for _ in range(n*m) ]
MOD = 9901
def dfs(i,sts):
	if i ==n*m:
		#print('sts:',sts)
		return 1

	if dp[i][sts]==-1:
		ret=0
		
		if sts & 1: #채워진 경우
			ret+= dfs(i+1,sts>>1)
		else:
			if i%m!=m-1 and not sts & 1<<1 : #각줄의 맨오른쪽이 아니고 그다음 블럭이 안채워진경우  1x2로 놓을수있음
				ret+= dfs(i+2, sts>>2)

			if i+m<n*m: #맨아랫줄이 아니면 2x1로 놓을 수 있음
				ret+= dfs(i+1, sts>>1 | (1<<(m-1)))	

		dp[i][sts] = ret%MOD

	return dp[i][sts]

dfs(0,0)
print(dp[0][0])


