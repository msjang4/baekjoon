import sys

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

inp=read().strip()

# string concatenation연산은 시간복잡도가 O(len)임
#s='#'
#for i in range(len(inp)):
#    s+=inp[i]
#    s+='#' #짝수 팰린드롬을 찾기위한 거
#따라서 join메소드를 이용해야함
s = f"#{'#'.join(inp)}#"

n= len(s)
dp = [0]*n
ans=0
l=-1
r=-1
for i in range(n):

    if i>r:
        size = 1
    else:
        size = min(r-i+1,dp[l+r-i])
        #center point는 l+r/2임 i'는 cp - (i-cp)이므로 2*cp-i = l+r-i로 i'를 구할 수 있음
        #[l,r]구간내는 팰린드롬이 보장되므로 i+size가 r+1일때부터 탐색해야하므로 r+1-i = size임

    while i-size >=0 and i+size<n and s[i-size] == s[i+size]:
        size+=1
    size-=1
    if i+size>r:
        r= i+size
        l= i-size
    dp[i] = size
    ans+= dp[i]//2 +dp[i]%2



print(ans)



