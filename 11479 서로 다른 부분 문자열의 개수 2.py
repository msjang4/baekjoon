import sys

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

s=read().strip()
n= len(s)
rank = [ord(c) for c in s]+[-1] #rank[i]는 접미사 문자열 si~sn의 순위임.

k=1
suf = [i for i in range(n)] #suf [i]는 순위가 i인 접미사 문자열을 가리킴

while k<=n:#log(n)
    # arr = [ (rank[i],rank[i+k]) if i+k < n else (rank[i],-1) for i in range(n)]
    # arr배열 만드는 과정을 없애서 O(NlogN)만큼 절약
    suf.sort(key=lambda i: (rank[i],rank[min(i+k,n)]) )
    tmp = [0]*(n+1) #새로운 rank배열을 임의로 저장
    tmp[-1] = -1     #rank[n]이 항상 -1이 되게 유지함
    #tmp[suf[0]] = 0

    for i in range(1,n): #O(n)
        pre,cur = suf[i-1], suf[i]
        if (rank[pre],rank[min(pre+k,n)]) != (rank[cur],rank[min(cur+k,n)]):
            tmp[cur] = tmp[pre]+1
        else:
            tmp[cur] = tmp[pre]

    rank = tmp
    k*=2
p=0
lcp = [0]*n
ans = (n+1)*n//2
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
    ans-=p
    p= max(0,p-1) #p줄이는데 0보다 작아지면 안됨.
    # si_sn 과 sj_sn이 공통접두사 길이가 p라면
    # si+1_sn은 sj+1_sn과 공통접두사길이가 p-1이므로 최소 p-1이란게 보장되는거임.

#접미사의 공통 접두사가 x라면 x의 부분문자열의 개수만큼 중복되는데
#그 개수는 x(x+1)/2고 이거는 1부터 x까지의 합이고 이건 lcp배열 구할때
# p가 1씩 작아지니깐 애초에 lcp배열내 x부터 1까지 있으니 lcp배열의 합을 빼면됨

print(ans)

