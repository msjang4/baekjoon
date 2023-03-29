import sys
try:
    read = open('stdout.txt', 'r').readline
except:
     read = sys.stdin.readline
# q_j, e_j 를 오른쪽 위 꼭짓점으로 하는 직사각형 중에 넓이가 가장 큰것
# 의 왼쪽 아래 꼭지점이 p_k,d_k라고 하자 -> 1번 가정
#
# p_k, d_k보다 왼쪽아래에 있는 점은 없다. 그점을 왼쪽꼭짓점으로하면 더큰 직사각형만들수있음
#
# q_j, e_j보다 왼쪽위에 있는 q_i, e_i를 생각해보자
#
# 이때 p_k,d_k보다 오른쪽 아래에 있는 어떤 임의의 점 p_l,d_l에 대해
#
# R(p_l,d_l, q_i,e_i) 보다 항상 R(p_k,d_k, q_i,e_i)가 크다
#
# R(p_k,d_k, q_j,e_j)와 R(p_l,d_l, q_i,e_i)를 그려보면 반드시 십자가가 생긴다.
# 그리고 그 십자가는 R(p_l,d_l, q_j,e_j)+ R(p_k,d_k, q_i,e_i)에 정확하게 포함된다.
# 즉 R(p_l,d_l, q_j,e_j)+ R(p_k,d_k, q_i,e_i) > R(p_k,d_k, q_j,e_j)와 R(p_l,d_l, q_i,e_i) 인데
# 7번가정에의해 R(p_l,d_l, q_j,e_j) < R(p_k,d_k, q_j,e_j) 이므로
# R(p_k,d_k, q_i,e_i)>  R(p_l,d_l, q_i,e_i)이다.
#
# q_j,e_j 보다 오른쪽아래에 있는 점은 반대로  p_k,d_k보다 왼쪽위에 있는 임의의점과 만든 직사각형은
# p_k,d_k와 만든 직사각형 보다 넓이가 작다.

# 분할정복을 쓸수 있을 것 같으나 q_j,e_j보다 오른쪽 위에 있는 점은 이런 분할 탐색을 적용할 수가 없다.
# 그럼 어떻게 해야되나? 사실 오른쪽위에 점이 있는 경우 절대 정답이 될 수 없다
# 그러니깐 오른쪽 위에 점이 없는 것들만으로 탐색해도 된다는뜻

m,n= map(int,read().split())

pdarr = [0]*m
qearr = [0]*n
for i in range(m):
    pdarr[i] = tuple(map(int,read().split()))

for i in range(n):
    qearr[i] = tuple(map(int,read().split()))

qearr.sort(lambda x: (x[1],x[0])) #오른쪽아래에서 왼쪽 위 순으로 정렬
pdarr.sort(lambda x: (x[1],x[0]))
stk = [qearr[0]]
size=1
for i in range(1,n):
    while size> 0 and stk[-1][0] <= qearr[i][0] and stk[-1][1] <= qearr[i][1]:
        #왼쪽아래에 점이 없도록 하면 모든 점의 오른쪽 위에는 점이 없게된다.
        stk.pop();size-=1;
    stk.append(qearr[i])
    size+=1
def getc(k,j):
    x1,y1 = pdarr[k]
    x2,y2 = stk[j]
    if y2-y1 < 0: #dy, dx둘다 -면 +가 돼버림
        return 0
    return (y2-y1)*(x2-x1)
ans=0

def dnc(l,r,s,e):
    global ans
    if l>r:
        return
    m = (l+r)//2
    maxidx = s
    for k in range(s+1,e+1):

        if getc(maxidx,m) < getc(k,m):
            maxidx  =k
    #print(stk[m],pdarr[maxidx],getc(maxidx,m))
    ans = max(ans, getc(maxidx,m))
    if l< r:
        dnc(l,m-1,s,maxidx)
        dnc(m+1,r,maxidx,e)

dnc(0,size-1,0,m-1)
print(ans)