import sys

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

s=read().strip()

n = len(s) #O(n)
rank = [0]*n #rank[i]는 접미사 문자열 si~sn의 순위임.
for i in range(n):
    rank[i] = ord(s[i]) - ord('a')

k=1
arr = [0]*n
suf = [i for i in range(n)] #suf [i]는 순위가 i인 접미사 문자열을 가리킴
while k<=n:#log(n)
    for i in range(n):
        #O(n)
        if i+k < n:#2*k길이 접두사를 비교하면 이전에 구해놓은 k길이 접두사 순위에서
            # i랑 i+k 순서쌍으로 비교할수 있다.
            arr[i]= (rank[i],rank[i+k])
        else:
            arr[i]= (rank[i],-1)
    suf.sort(key=lambda x: arr[x])
    rank[suf[0]] = 0
    cnt=0
    for i in range(1,n): #O(n)
        if arr[suf[i]] != arr[suf[i-1]]: #이전 순위의 튜플이랑 틀려야 순위가 올라감
            cnt+=1
        rank[suf[i]] = cnt #이번순위의 랭크를 셋
    #print(rank)
    k*=2
p=0
lcp = [0]*n
lcp[0]='x'
for i in range(n): #O(n)
    #rank[i] 가 si~sn 접미사 문자열의 순위고
    #얘랑 비교할건 순위가 rank[i]-1인 접미사문자열이니까
    #suf[rank[i]-1]임.

    if rank[i]==0:
        continue

    j = suf[rank[i]-1]
    while i+p<n and j+p <n and s[i+p] == s[j+p]: #공통 접두사 크기구함.
        p+=1
    lcp[rank[i]] =p

    p= max(0,p-1) #p줄이는데 0보다 작아지면 안됨.
    # si_sn 과 sj_sn이 공통접두사 길이가 p라면
    # si+1_sn은 sj+1_sn과 공통접두사길이가 p-1이므로 최소 p-1이란게 보장되는거임.
for i in range(n):
    suf[i]+=1
print(*suf)
print(*lcp)

