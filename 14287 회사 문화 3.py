import sys
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10**5)
n, m = map(int,read().split())

from math import log2, ceil
size= 2**(ceil(log2(n)))
adj = [[] for  i in range(n+1)]

for u, boss in enumerate(map(int, read().split()[1:]),start=2): #1번 제외하고 2번부터
    adj[boss].append(u)

#mmu 1장 더

def euler_tour(u): #오일러투어테크닉을 통해 각 노드들의 자식을 일련된 구간으로 바꿀 수 있다.
    global idx
    euler[u] = idx #u번 노드가 트리전체에서 몇번째로 방문됐는지

    idx+=1
    for v in adj[u]:
        euler_tour(v)
    childs[u]=idx-1 # 마지막 자식노드의 인덱스




def update(i,d):
    i = size+i #i번직원 노드 인덱스를 구함
    while i: #logn
        segtree[i]+=d
        i//=2



def query(l,r,i=1,b=0,e=size-1):
    if r < b or e < l:  # [b,e]구간과 [l,r]구간이 전혀 겹치지 않는경우
        return 0
    if l <= b and e <= r:  # [b,e]구간이 [l,r]구간에 완전속하는 경우
        return segtree[i]
    elif i<size: #리프아닌경우
        m = (b + e) // 2
        return query( l, r, i * 2,b, m)+query( l, r, i * 2 + 1,m + 1, e)
    return 0

euler = [0]*(n+1) #i번 노드가 오일러투어에서 몇번째로 방문한 노드인지
# i번직원의 노드의 인덱스는 size+euler[i]가 됨.
idx =0
childs= [0]*(n+1)# i번 직원이 칭찬받은정도는 euler[i]~childs[i]까지의 구간합
euler_tour(1)

segtree = [0]*(2*size) # 이렇게 선언하면 인덱스가 size이상이면 리프노드임.
lazy = [0]*(2*size)
for _ in range(m):
    fc, *param = map(int, read().split())
    if fc ==1:#칭찬
        i,w = param
        update(euler[i],w)
    elif fc ==2:
        i = param[0]
        ans=query(euler[i],childs[i])
        print(ans)

