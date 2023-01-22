import sys
from math import ceil
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**5)
n,m = map(int,read().split())

arr = [0]+[*map(int, read().split())]

cnt = [0]*(1_000_000+1) # i번 수의 개수


querys = [(*map(int,read().split()),i) for i in range(m)]

def add(l,r):
    global ans

    for i in range(l,r):
        cnt[arr[i]] +=1
        ans += arr[i] * (cnt[arr[i]] ** 2 - (cnt[arr[i]]-1)**2)


def erase(l,r):
    global ans
    for i in range(l, r):
        cnt[arr[i]] -=1
        ans += arr[i] * (cnt[arr[i]] ** 2 - (cnt[arr[i]]+1)**2)

rootn = n**0.5
querys.sort(key= lambda x: (x[0]//rootn, x[1]) )


ans_li = [0]*m
ans=0

add(querys[0][0], querys[0][1]+1) #r+1을 해줘야 r까지 다 더해짐 ㅇㅇ
ans_li[querys[0][2]] = ans
for i in range(1,m):
    add(querys[i][0], querys[i-1][0]) #l이 더작아져야 추가됨
    erase(querys[i-1][0],querys[i][0])

    #r은 더커져야 추가됨.
    add(querys[i-1][1]+1, querys[i][1]+1) # ~2구간에서 ~5구간이되면 3~5까지더해야하므로 3,6을넘김
    erase(querys[i][1]+1, querys[i-1][1]+1) # ~5구간에서 ~2구간이되면 3~5구간을 삭제해야하므로

    ans_li[querys[i][2]] = ans
for ans in ans_li:
    print(ans)
