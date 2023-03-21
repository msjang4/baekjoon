import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n,d = map(int,read().split())

# dp [j] = j번째날에 김치를 꺼낼때 가장 맛있는 김치
# max for k<j: v[k] + c[k][j]
# c[k][j] = (j-k)*T[j]
# c[a][d] + c[b][c] 는 (d-a)*t[d] + (c-b)*t[c]
#   = (b-a)*t[d] + (d-c)*t[d]+  (c-b)*t[d] + (c-b)*t[c]
# c[a][c] + c[b][d] 는 (c-a)*t[c] + (d-b) * t[d]
#    = (c-b)*t[c] + (b-a)*t[c] + (d-c)*t[d] + (c-b)*t[d]
#    = (b-a)*t[c] + (d-c)*t[d] + (c-b)*t[d] + (c-b)*t[c]
# 이때 d > c이므로 t[d] <= t[c]이다. 즉, monge array라는 뜻
# 즉, dnc 트릭을 쓸수있다.

t = [*map(int, read().split())]
v = [*map(int, read().split())]

def getc(k,j):
    return (j-k)*t[j]
ans = 0
def dnc(l,r,s,e):
    global ans
    m = (l+r)//2
    ls = max(s,m-d) #s를 제한함 d범위에서
    le = min(m,e) #e를 제한함

    maxidx = ls
    for k in range(ls+1,le+1):

        if v[maxidx] + getc(maxidx,m) < v[k] + getc(k,m):
            maxidx  =k
    ans = max(ans, v[maxidx] + getc(maxidx,m))
    if l< r:
        dnc(l,m-1,s,maxidx)
        dnc(m+1,r,maxidx,e)

dnc(0,n-1,0,n-1)

print(ans)

