import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

# 특공대 하나의 전투력은 ax^2 + bx + c이므로
# 특공대가 몇개 편성되던 bx의 합은 b(sum)으로 동일하다.
# 즉, 특공대별 ax^2+c합만 최대로 하면되고 이는 특공대별 -ax^2-c 합의 최솟값 구하는 것과 동일하다.

# dp[i]를 i번 대원까지 만들 수 있는 전투력 최댓값이라 할때
# min_for j< i : -(a(x-s_j)^2 - c + dp[j] 고
# 식을 풀어보면 -a(x^2 -2xs_j +s_j^2) - c +dp[j]
#            이때 x^2, c는 공통부분이므로
# min_for j< i : 2as_j x - as_j^2 + dp[j] 과 같다.
# 즉 계수가 2as_j인데 j가클수록 s_j가 크고 a가 음수이므로
# 계수는 j가 클수록 작아진다. 따라서 컨벡스헐 트릭을 쓰면 끝!!


def get_cross_x(sj1,dpj1,sj2,dpj2):
    a1, b1 = 2 * a * sj1, -a*sj1 ** 2 + dpj1 #15행 주석 참고
    a2, b2 = 2 * a * sj2, -a*sj2 ** 2 + dpj2#15행 주석 참고

    return (b2-b1)/(a1-a2)


def search(x):
    b,e =0,size-1

    while b<e:
        m = (b+e)//2
        if get_cross_x(*stk[m],*stk[m+1]) < x:
            b = m+1
        else:
            e= m

    sj,dpj =stk[b]
    ret = -a*(x-sj)**2-c+dpj #9번 행 주석 참고
    return ret



n= int(read())

a,b,c = map(int,read().split())

arr = [*map(int,read().split())]


s = 0
stk =[(0,0)] #(sj,dpj)의 튜플로 넣을건데 맨처음에 (0,0)을 넣어줘야함.
size = 1
for i in range(n):
    s+=arr[i]
    t = (s,search(s))
    while size >1 and get_cross_x(*stk[-2],*stk[-1]) > get_cross_x(*stk[-2],*t):
        stk.pop();size-=1
    stk.append(t)
    size+=1
print(-stk[-1][1]+b*s)
