'''input
4 4
ACFC
FDAB
BACF
DBAC
'''
import sys
from pprint import pprint
read = sys.stdin.readline
sys.setrecursionlimit(10**5) #dfs 최대 깊이 2^14 = 16384
n,m = map(int, read().split())
mp = ''.join([read().strip() for _ in range(n)])

#print(mp)
size = 2**m
dp = [[-1]*size for _ in range(n*m) ]
score = [
[10,8,7,5,1],
[8,6,4,3,1],
[7,4,3,2,1],
[5,3,2,2,1],
[1,1,1,1,0]
]
def get_score(i,j): #두 칸의 두부 가격을 구하는 함수
	a=ord(mp[i])-ord('A')
	b= ord(mp[j])-ord('A')
	if a>4:
		a=4
	if b>4:
		b=4
	return score[a][b]

def dfs(i,sts):
	if i ==n*m:
		#print('sts:',sts)
		return 0

	if dp[i][sts]==-1:
		
		dp[i][sts]= max(dp[i][sts],dfs(i+1,sts>>1))
		
		if not sts & 1: #안채워진 경우
	
			if i%m!=m-1 and not sts & 1<<1 : #각줄의 맨오른쪽이 아니고 그다음 블럭이 안채워진경우  1x2로 자를수있음
				dp[i][sts] = max(dp[i][sts],dfs(i+2, sts>>2)+get_score(i,i+1))

			if i+m<n*m: #맨아랫줄이 아니면 2x1로 자를 수 있음
				dp[i][sts]= max(dp[i][sts],dfs(i+1, sts>>1 | (1<<(m-1)))+get_score(i,i+m))


	return dp[i][sts]

dfs(0,0)
print(dp[0][0])


