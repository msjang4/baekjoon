import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline



n,k =map(int,read().split())

arr= [ int(read()) for _ in range(n)]
arr.sort()
def parametric(l,r):
	if l>r:
		return 0

	m = (l+r)//2

	prev = -1
	cnt = 0
	for x in arr:
		if prev ==-1 or x - prev >= m:
			cnt +=1
			prev = x


	if cnt >= k:
		return max(m,parametric(m+1,r))
	else:
		return parametric(l,m-1)

ans= parametric(0,1000_000_000)
print(ans)
