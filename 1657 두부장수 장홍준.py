'''input
3 3
AAA
AFA
AAA
'''
import sys
read = sys.stdin.readline
sys.setrecursionlimit(10**5) #dfs 최대 깊이 2^14 = 16384
n,m = map(int, read().split())
size = 2**m

mp = [read().strip() for _ in range(n)]

score = [
[10,8,7,5,1],
[8,6,4,3,1],
[7,4,3,2,1],
[5,3,2,2,1],
[1,1,1,1,0]
]
def get_scores(i,x):
	ret=0
	for k in range(m):
		if x & (1<<k):
			ret+= get_score(mp[i][k], mp[i-1][k])

	return ret

def get_scores_line(i,x): #한줄에서 1x2씩 총 x만큼 잘랐을때 
	ret=0
	k=0
	while k<m:
		if k<=m-2 and x & (1<<k):
		#	print(i,k)
			ret+=get_score(mp[i][k],mp[i][k+1])
			k+=2
		else:
			k+=1

	return ret

def get_score(a,b): #두 칸의 두부 가격을 구하는 함수
	a=ord(a)-ord('A')
	b= ord(b)-ord('A')
	if a>4:
		a=4
	if b>4:
		b=4
	return score[a][b]

dp= [[0]*(size)    for _ in range(n)]
#dp[i][j] := nxm 에서 nxi까지 사용하고 i+1번째 줄을 bin(j)까지 사용하여 잘랐을때 가격의 최댓값

#dp[0] (초기식)을 채우는 재귀함수 (dfs형식)
arr=[]
def dfs(i,x,val):
	#print(i,x,val)
	if i==m:
		dp[0][x]=val
		arr.append(x)
		return
	dfs(i+1,x,val) #두부를 자르지 않음
	if i<=m-2:
		dfs(i+2,x|(3<<i),val+get_score(mp[0][i],mp[0][i+1])) #1x2로 자름
dfs(0,0,0)

for i in range(n):
	for j in range(size):
		for k in range(m):
			dp[i][j] = max(dp[i][j],dp[i][j&~(1<<k)]) #k번째 비트가 0인경우  -> i+1번째 줄 k번째 두부를 미사용하는 경우 

		if i==0: 
			continue

		dp[i][j] = max(dp[i-1][~j] + get_scores(i,j),dp[i][j])
		
		for x in arr:
			if not j & x: #겹치는 거 없으면
				# nxm 에서 nxi까지 사용하고 i+1번째 줄을 bin(j)까지 사용했고 1x2로 된 블럭들로 다시 i+1번째 줄을 채워서 j|x까지 사용한 경우
				dp[i][j|x] = max(dp[i][j|x],dp[i][j]+get_scores_line(i,x))


print(dp[-1][-1])


