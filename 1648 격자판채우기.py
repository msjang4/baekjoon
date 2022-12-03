'''input
14 14
'''
import sys
read = sys.stdin.readline
sys.setrecursionlimit(10**5) #dfs 최대 깊이 2^14 = 16384
n,m = map(int, read().split())
size = 2**n 

dp= [[0]*(size) for _ in range(m)]
#dp[i][j] := nxm 에서 nxi까지 다채우고 i+1번째 줄에는 bin(j)로 채우는 경우의 수


#dp[0] (초기식)을 채우는 재귀함수 (dfs형식)
arr=[]
def dfs(i=0,x=0):
	#print(i,x)
	
	if i==n:
		dp[0][x] = 1
		arr.append(x)
		return
	dfs(i+1,x) #블록을 놓지 않음.
	if i<=n-2:
		dfs(i+2,x|(3<<i)) #1x2로 붙임.
dfs()


MOD= 9901
for i in range(1,m):
	for j in range(size):
		tmp = dp[i-1][~j] 
		for x in arr:
			if not j & x: #겹치는 거 없으면
				# nxi-1까지 다채우고 i번째 줄에 bin(~j)로 채운 거에 
				# 2x1로 된 블럭들을 채워서 nxi까지 다채우고 i+1번째 줄을 bin(j)로 채우고 
				# 1x2로 된 블럭들로 다시 i+1번째 줄을 채우는 경우
				dp[i][j|x] = (dp[i][j|x] + tmp)%MOD

print(dp[-1][-1])


