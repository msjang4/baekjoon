'''input
8
2 3
3 1
3 2
1 1
1 2
1 3
2 1
2 2
'''
import sys
from math import ceil, log2
from functools import cmp_to_key

read = sys.stdin.readline
n = int(read())

arr = [list(map(int,read().split())) for _ in range (n)]

arr.sort() #먼저 좌표 순으로 정렬 , 좌표순으로 먼저 정렬 해야 변에 점이 여러 개 있는 경우를 처리 가능

std=arr[0] #첫번째 좌표를 기준점으로 선정

def ccw(p1,p2,p3):
	a = p2[0] - p1[0]
	b = p2[1] - p1[1]
	c = p3[0] - p1[0]
	d = p3[1] - p1[1]
	return a*d-b*c

#기준점과의 ccw 값으로 나머지 점들을 정렬
arr = sorted(arr[1:], key = cmp_to_key(lambda p1,p2: -ccw(std,p1,p2) ))

stk = [std,arr[0]] #
i=1
for i in range(1,n-1): #기준점 제외 n-1개 
	nex = arr[i]
	while len(stk)>=2:
		sec = stk.pop()
		fir = stk[-1] # fir,sec,nex의 ccw값에 상관없이 어차피  fir는 다시 스택에 들어가므로
		#pop하지 않고 top으로 값만 추출

		if ccw(fir,sec,nex)>0: #변에 점이 여러 개 있는 (= 평행한) 경우에는 가장 양 끝 점만 개수에 포함 
			stk.append(sec)  #fir, sec,next가 반시계방향이라 sec를 convex hull 요소로 넣는 것.
			break
		# fir,sec,next가 시계방향이면 while문을 한번더 돌게 되고 그때는 fir가 sec가 되고 fir이전게 fir가 됨.
		#근데 stk에 2개 이상없으면 그만둠.
		
	stk.append(nex)
print(len(stk))


