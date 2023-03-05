import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

n= int(read())
a = [*map(int,read().split())]
b = [*map(int,read().split())]
dp = [0]*n
#dp[j] = j번 나무를 자를때 최소비용
# dp[j] =  b[i]*a[j] +dp[i] for i<j 이므로 컨벡스헐 트릭 쓰면됨


ans= dp[-1]



def search(x): #parametric search
    s,e=0,size-1
    while s<e:
        m= (s+e)//2
        if get_cross_x(stk[m],stk[m+1]) <x:
            s=m+1
        else:
            e=m



    return stk[s]

def get_cross_x(i,j):

    q,r= b[i],dp[i]
    u,v = b[j],dp[j]
    x= (v-r)/(q-u)
    return x

stk= [0]
size=1
for j in range(1,n):
    k= search(a[j]) #이진탐색으로 1차함수구함
    dp[j] = b[k]*a[j]+dp[k] #최소비용계산

    #컨벡스헐 업데이트
    while size>1 and get_cross_x(stk[-2],stk[-1]) > get_cross_x(stk[-1],j):
        stk.pop()
        size-=1
    stk.append(j)
    size+=1

print(dp[-1])

