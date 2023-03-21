import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

l,g = map(int,read().split())
c= [*map(int,read().split())]
#g를 간수로 보기보단 탈옥수들을 몇개의 그룹으로 나눌건지로 생각하면 좋다
# dp [g][l] l번 감옥까지 g개의 간수를 배치 = g개의 그룹으로 나눳을때
# 최소 탈옥 위험도
# min for k < l: dp[g-1][k] + c[k][l]

# c[k][l] = (l-k) * sum_kl  sum kl은 k+1번감옥부터 l번감옥까지 탈옥력 합
#
# c[a][d] + c[b][c]
# a-b 구간 x (d-a)
# b-c 구간 x (d-a) + (c-b) = (d+c -a-b)
# c-d 구간 x (d-a)

# c[a][c] + c[b][d]
# a-b구간 x (c-a)
# b-c 구간 x (c-a) + (d-b) = (d+c - a-b)
# c-d 구간 x (d-b)
# 즉 monge array를 만족 , dnc를 써봅시다!

presum = [0]*l
dp = [0]*l
s=0
for i in range(l):
    s+= c[i]
    presum[i] = s
    dp[i] = s*(i+1)


def getc(k,j):
    return (j-k)*(presum[j] - presum[k])

tmp = [0]*l
def dnc(l,r,s,e):
    if l > r:
        return

    m = (l+r)//2
    le = min(m,e) #e를 제한함

    minidx = s
    for k in range(s+1,le+1):

        if dp[minidx] + getc(minidx,m) > dp[k] + getc(k,m):
            minidx  =k

    tmp[m] = dp[minidx] + getc(minidx,m)

    dnc(l,m-1,s,minidx)
    dnc(m+1,r,minidx,e)

for _ in range(g-1):
    dnc(0,l-1,0,l-1)
    for i in range(l):
        dp[i] = tmp[i]
print(dp[-1])