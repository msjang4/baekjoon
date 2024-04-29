"""input
5886899678
7
2 6 9
1 2 9 8 5
1 1 3 5 0
2 1 6
1 1 10 0 2
1 5 8 8 1
2 1 10
"""
import sys
import math
read = sys.stdin.readline
S = read().strip()
# S = '1234567890'*(10**5)
N = len(S)
LOG = math.ceil(math.log2(N))
FIRST_LEAF = LEAF_CNT= 2**LOG
OFFSET = LEAF_CNT-N-1
mod_arr = [10]*LOG

print(LOG)
segtree = [[0]*(2**(LOG+1)) for _ in range(10)]
lazy = [[-1]*(2**(LOG+1)) for _ in range(10)]

#lazy값, 나머지 값 
#

MOD = 998_244_353
Q = int(read())
for i,c in enumerate(S, start=1):
    segtree[int(c)][FIRST_LEAF+OFFSET+i] = 1

# 이제 부모의 나머지값 계산할텐데 이때 그냥 *(10**x)해버리면 안됨
# 10 ** (2** x) % MOD를 배열에 미리 구해놓음.
for i in range(LOG-2, -1,-1):
    mod_arr[i] = mod_arr[i+1]*mod_arr[i+1]%MOD
# 그리고 ((왼쪽 자식 나머지값 * MOD 값) + 오른쪽 자식 나머지값) % MOD 을 해줘야함

print(mod_arr)
def init(num, node_idx, depth=0):
    if node_idx < FIRST_LEAF:
        l = init(num,node_idx*2, depth+1)
        r = init(num,node_idx*2+1, depth+1)
        segtree[num][node_idx] = (l*mod_arr[depth] + r) %MOD
        
    return segtree[num][node_idx]


def serialization(fr, to, node_idx):
    # 행동들이 실행되는 순서에 상관없도록 직렬화를 시켜준다.
    # 즉 fr->to 변경시 0~9중에 fr로 바뀌는게 있다면 그 행동을 to로 바뀌는걸로 취급
    # 만약 to가 무언가로 바뀌는게 있다면 얘는 어쩔 수 없이 전파시켜야함

    for c in range(2):
        if lazy[to][node_idx*2+c] != -1:
            propagate(to, node_idx*2+c)

    for num in range(10):
        for c in range(2):
            if lazy[num][node_idx*2+c] == fr: 
                lazy[num][node_idx*2+c] = to

def propagate(fr, node_idx):
    if to :=lazy[fr][node_idx] != -1:
        segtree[to][node_idx] = (segtree[to][node_idx] + segtree[fr][node_idx])%MOD
        segtree[fr][node_idx] = 0
        lazy[fr][node_idx] = -1
        if node_idx < FIRST_LEAF:
            serialization(fr, to, node_idx)

def sub_query(num, i, j, node_idx, l, r, depth):

    propagate_all(node_idx)

    if r < i or j < l : # 전혀 겹치지 않는 경우
        return 0

    if i <= l and r <= j: # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우
        return segtree[num][node_idx]
    
    elif node_idx < FIRST_LEAF:
        m= l+r>>1

        lquery = sub_query(num,i,j, node_idx*2, l, m, depth+1)
        rquery = sub_query(num, i,j, node_idx*2+1, m+1, r , depth+1)

        return (lquery*mod_arr[depth] + rquery)%MOD
    
    else: #여기서 else는 뭔가 잘못된 거
        assert(0)
    


def propagate_all(node_idx):
    for num in range(10):
        propagate(num, node_idx)


def update(i,j, node_idx, l,r, fr, to, depth):

    propagate_all(node_idx)
    
    if r < i or j < l : # 전혀 겹치지 않는 경우
        return 0

    if i <= l and r <= j: # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우
        lazy[fr][node_idx] = to
        propagate(fr, node_idx)
    
    elif node_idx < FIRST_LEAF:
        m= l+r>>1
        update(i,j, node_idx*2, l,m, fr, to, depth+1)
        update(i,j, node_idx*2+1, m+1,r, fr,to, depth+1)
    
    else: #여기서 else는 뭔가 잘못된 거
        assert(0)




def query(i,j):

    remainder = 0
    for num in range(1,10):
        remainder = (remainder+sub_query(num, i, j, 1, 0, LEAF_CNT-1,0)*num) %MOD

    return remainder



for num in range(10):
    init(num, 1)

# print(segtree[8])
# for num in range(10):
#     print(segtree[num])
for _ in range(Q):
    c,*x = read().split()
    if c == '1':
        i,j,fr,to = map(int, x)
        if fr == to: #fr =to는 그냥 걸러버리자
            continue
        update(i+OFFSET,j+OFFSET,1, 0, LEAF_CNT-1,fr,to, 0)
        pass

    elif c== '2':
        
        i,j = map(int,x)
        print(query(i+OFFSET,j+OFFSET))
        pass
    
