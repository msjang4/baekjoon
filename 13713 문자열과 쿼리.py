import sys

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

s=read().strip()
s=list(reversed(s)) #공통 접미사를 구하므로 그냥 뒤집으면 끝

n= len(s)
dp = [0]*n #zarray
dp[0] = n
l=0
r=-1
for i in range(1,n):

    if i>r:
        size = 0
    else:
        size = min(r-i+1,dp[i-l])
        #i'는 i-l이고
        #[l,r]구간내는 보장되니깐 i+size가 r+1일때부터 탐색해야하므로 r+1-i = size임

    while i+size<n and s[size] == s[i+size]:
        size+=1
    if i+size>r:
        r= i+size-1
        l= i
    dp[i] = size

m= int(read())
for _ in range(m):
    #처음에 뒤집어서 인덱스도 음수로 접근하면됨.
    print(dp[-int(read())])



