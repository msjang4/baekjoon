import sys
from math import ceil,log2
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**2)
n,k,d = map(int,read().split())

arr = [*map(int, read().split())]

size = 2**ceil(log2(5*10**5+1))
segtree= [0]*(2*size)
#segtree[size+i]는 숫자 i로 끝나는 부분수열A중 최대길이고
#segtree는 maxtree
mod= [0]*(5*10**5) #mod[i]는 마지막 숫자의 %k값이 i인 부분수열 A들중 최대길이

def update(i,d): #logn
    i = size+i
    segtree[i] =d
    while i:
        i>>=1
        segtree[i] = max(segtree[i*2],segtree[i*2+1])

def query(l,r,i=1,b=0,e=size-1): #logn
    if r<b or e<l:
        return 0;

    if l<=b and e <= r:
        return segtree[i]
    elif i< size:
        m= (b+e)//2
        return max(query(l,r,i*2, b,m),query(l,r,i*2+1,m+1,e))
    else:
        return 0

update(arr[0],1)
mod[arr[0]%k] = 1
for i in range(1,n):
    r = arr[i]%k
    maxlen = max(mod[r],query(arr[i]-d,arr[i]+d))+1
    mod[r] = max(maxlen, mod[r])
    if maxlen > segtree[size+arr[i]]:
        update(arr[i],maxlen)
print(query(0,size-1))
