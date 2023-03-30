import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline


n ,m,k = map(int,read().split())


arr = [list(read().strip())for _ in range(n)]

oddarr = [ [0]*(m+1) for _ in range(n+1)]
evenarr = [ [0]*(m+1) for _ in range(n+1)]

for i in range(1,n+1):
    for j in range(1,m+1):
        #짝수칸끼리 홀수칸끼리 2차원 누적합 구함.
        oddarr[i][j] = oddarr[i-1][j]+oddarr[i][j-1]-oddarr[i-1][j-1] +(arr[i-1][j-1] =='B' and (i+j)%2==0)

        evenarr[i][j] = evenarr[i-1][j]+evenarr[i][j-1]-evenarr[i-1][j-1] +(arr[i-1][j-1] =='B' and (i+j)%2)

even_cnt = k*k//2
odd_cnt = k*k - even_cnt
ans=k*k
for i in range(k,n+1):
    for j in range(k,m+1):
        odds = oddarr[i][j] - oddarr[i-k][j] -oddarr[i][j-k] +oddarr[i-k][j-k]
        evens = evenarr[i][j] -evenarr[i-k][j] - evenarr[i][j-k] + evenarr[i-k][j-k]
        if (i+j)%2: # 짝수번째 칸이면 odd ,even이 바뀌어야함
            odds,evens = evens,odds
        ans = min(ans, min(odd_cnt-odds+evens, even_cnt-evens+odds))

print(ans)

#홀수 대각선의 합, 짝수 대각선의 합이렇게 있을때
#홀수 대각선 전부 1로 홀수 대각선 칸 수 - 홀수대각선의합 + 짝수 대각선합
#짝수 대각선 전부 1로 짝수 대각선 칸 수 - 짝수대각선 합 + 홀수 대각선 합