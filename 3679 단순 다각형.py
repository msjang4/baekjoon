import sys
from bisect import bisect_left
debug = True
if debug:
    read = open('stdout.txt','r').readline
else:
    read = sys.stdin.readline




def slope(p1,p2):
    #p1 -> p2 일때 dy/dx
    if p1[0]==p2[0]:
        return float('inf')
    else:
        return (p2[1]-p1[1])/(p2[0]-p1[0])



def concave(arr):
    n=len(arr)
    arr.sort()  # 좌표 정렬
    std = arr[0][0]  # 좌표가 가장 작은 점을 기준점으로해야 dy/dx 순으로 정렬시 반시계방향으로 정렬됨
    stdidx = arr[0][1]
    li =sorted([(slope(x,std),i) for x,i in arr[1:]],key =lambda x:x[0]) #기준점과의 기울기로 정렬

    maxidx = bisect_left(li,li[-1][0],key=lambda x:x[0])#가장 기울기가 큰 점 중 기준점과 가장 가까운 점의 idx
    #bisect_left에 key 파라미터는 python 3.10에 추가돼서 pypy3에서는 type error가 남.

    return stdidx,li, maxidx
t = int(read())
for _ in range(t):
    tmp=list(map(int,read().split()))
    arr=[]
    for i in range(1,len(tmp),2):
        arr.append(([tmp[i],tmp[i+1]],i//2))
    stdidx, li,maxidx= concave(arr)
    print(stdidx,end =' ')
    for s,i in li[:maxidx]:
        print(i,end=' ')
    for s,i in reversed(li[maxidx:]): #기울기가 가장 큰점들은 기준점 쪽으로 연결해야 되므로 순서가 반대여야함.
        print(i,end=' ')
    print()








