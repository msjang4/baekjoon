import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**5)
n = int(read())

from math import log2, ceil
size= 2**(ceil(log2(n)))

def propagate(i,b,e):

    if lazy[i]:
        if (e-b+1)%2:
           segtree[i] ^= lazy[i]
        if i < size:
            lazy[i*2] ^= lazy[i]
            lazy[i*2+1] ^= lazy[i]
        lazy[i] = 0
def init(i=1):
    if i< size:
        init(i*2); init(i*2+1);
        segtree[i] = segtree[i*2] ^ segtree[i*2+1]

def update(l,r,d,i=1, b=0,e=size-1): #[l,r]구간을 d만큼 업뎃시킴 , b,e는 현재 노드 i가 관리하는 구간임
    propagate(i, b, e)  # lazy배열을 전파!
    #업데이트에서 lazy 전파를 하지않으면
    # 자식노드들의 lazy가 있더라도 실제값이 0이라서 41번줄에 segtree[i]가 0이될수도 있다.
    if r<b or e < l :#[b,e]구간과 [l,r]구간이 전혀 겹치지 않는경우
        return
    if l<=b and e <= r: #[b,e]구간이 [l,r]구간에 완전속하는 경우
        if (e-b+1) %2: # 어떤 수 x를 짝수번 xor하면 0임

            segtree[i] ^= d
        if i< size: #리프 아닌경우
            lazy[i*2] ^=d
            lazy[i*2+1]^=d
    elif i<size: #리프아닌경우
        m= (b+e)//2
        update(l,r,d,i*2,b,m)
        update(l,r,d,i*2+1,m+1,e)
        segtree[i] = segtree[i*2] ^ segtree[i*2+1]


def query(l,r,i=1,b=0,e=size-1):
    propagate(i, b, e) #lazy배열을 전파!
    if r < b or e < l:  # [b,e]구간과 [l,r]구간이 전혀 겹치지 않는경우
        return 0
    if l <= b and e <= r:  # [b,e]구간이 [l,r]구간에 완전속하는 경우
        return segtree[i]
    elif i<size: #리프아닌경우
        m = (b + e) // 2
        return query( l, r, i * 2,b, m)^query( l, r, i * 2 + 1,m + 1, e)
    return 0


segtree = [0]*(2*size) # 이렇게 선언하면 인덱스가 size이상이면 리프노드임.
lazy = [0]*(2*size)
segtree[size:size+n] = list(map(int,read().split()))
init()
m = int(read())
for _ in range(m):
    fc, *param = map(int, read().split())
    if fc ==1:#칭찬
        b,c,d = param
        update(b,c,d)
    elif fc ==2:
        b,c = param
        ans = query(b,c)
        print(ans)
