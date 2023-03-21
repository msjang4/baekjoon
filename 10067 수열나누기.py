import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

# 두원소 v,w가 서로다른 구간이면 점수에 v*w가 더해지는거고
# 아니라면 v*w는 안더해짐. 그니깐 어떤 순서로 자르던간에 상관이없다.
# 중간을 먼저자르던 왼쪽부터 자르던 말이다.
#
# dp[k][i]를 i번째 원소까지 k번 나눳을때 최댓값*-1 이라하면
# min for j<i : dp[k-1][j] - (x-s_j)*(s-x)
#            :  dp[k-1][j] - (sx - x^2  -s_js +s_jx)
#            : dp[k-1][j] - ((s+s_j)x - s_js - x^2)
    # j에대한 변수가 아닌것이 s랑 x이므로 sx랑 x^2을 빼주면된다.
# min for j< i :  - s_jx +s_js + dp[k-1][j]
def get_cross_x(j1,j2):
    a1, b1 = sarr[j1], sarr[j1] *_sum +dp[j1]#17번행 주석
    a2, b2 = sarr[j2], sarr[j2] *_sum + dp[j2]
    return (b2-b1)/(a2-a1)

def search(x):
    global p
    #x = s_i가 계속 증가하므로 logn 안찾아도 된다.
    #amortized O(1)
    while size-1 > p and get_cross_x(stk[p], stk[p + 1]) < x:
        p+=1
    return stk[p]

    # while b<e: # log(n)으로 시간초과발생
    #     m = (b+e)//2
    #     if get_cross_x(stk[m],stk[m+1]) < x:
    #         b = m+1
    #     else:
    #         e= m
    #
    # j=stk[b]
    # return j



n,k= map(int,read().split())

arr = [*map(int,read().split())]
_sum = sum(arr)
dp = [0]*n
sarr = [0]*n
s = 0
minidx=0
for i in range(n-1):
    s+= arr[i]
    sarr[i] = s
    dp[i] = -s*(_sum-s)
sarr[-1] = s+arr[-1]
m = [[0]*n for _ in range(k-1)]
stk = [0]*n
for l in range(k-1):
    tmp=[0]*n
    stk[0] = l 
    size = 1
    p=0
    for i in range(l+1,n-1): #l번째 원소까지 l+1번 나눌수 없음 ex) l=2 [0,1,2]를 3번나눌수 없음
        j = search(sarr[i])
        ret = dp[j] -(sarr[i]-sarr[j])*(_sum-sarr[i]) #13번 행 주석 참고
        m[l][i] = j
        tmp[i] =ret
        if arr[i] ==0:
            continue
        while size >1 and get_cross_x(stk[size-2],stk[size-1]) > get_cross_x(stk[size-1],i):
            size-=1
        stk[size]=i
        size+=1
    dp = tmp
l=k-2

for i in range(1,n):
    minidx = i if dp[i] < dp[minidx] else minidx  # minidx업데이트
i=minidx
print(-dp[i])
li = [0]*(k-1)
while l>=0: #백트랙킹
    li[l] = i+1
    i=m[l][i]
    l-=1
print(i+1,*li)