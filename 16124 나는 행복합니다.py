"""input
-
2
1 757395 866251 3 1
2 569101 862445
1 292308 948372 3 6
2 366834 522889
"""
import sys
import math
read = sys.stdin.readline
# print = sys.stdout.write
S = read().strip()
# S = '1234567890'*(10**5)
N = len(S)
LOG = math.ceil(math.log2(N))
FIRST_LEAF = LEAF_CNT= 2**LOG
OFFSET = LEAF_CNT-N-1
mod_arr = [1]*(10**6)

segtree = [[0]*(2**(LOG+1)) for _ in range(10)]
lazy = [[-1]*(2**(LOG+1)) for _ in range(10)]

#lazy값, 나머지 값 
#

MOD = 998_244_353
Q = int(read())
for i,c in enumerate(S, start=1):
    segtree[int(c)][FIRST_LEAF+OFFSET+i] = 1

# 이제 부모의 나머지값 계산할텐데 이때 그냥 *(10**x)해버리면 안됨
# MOD를 배열에 미리 구해놓음.
for i in range(1,N):
    mod_arr[i] = mod_arr[i-1]*10%MOD

# 그리고 ((왼쪽 자식 나머지값 * MOD 값) + 오른쪽 자식 나머지값) % MOD 을 해줘야함

# print(mod_arr)
def init(num, node_idx, l,r):
    if node_idx < FIRST_LEAF:
        m= l+r>>1
        lnode = init(num,node_idx*2,l,m)
        rnode= init(num,node_idx*2+1, m+1,r)
        segtree[num][node_idx] = (lnode*mod_arr[r-m] + rnode) %MOD
        
    return segtree[num][node_idx]


def serialization(fr, to, node_idx):
    # 행동들이 실행되는 순서에 상관없도록 직렬화를 시켜준다.
    # 즉 fr->to 변경시 0~9중에 fr로 바뀌는게 있다면 그 행동을 to로 바뀌는걸로 취급
    # 만약 to가 무언가로 바뀌는게 있다면 얘는 어쩔 수 없이 전파시켜야함
    # 이미 fr이 무언가로 바뀐다면 덮어씌울 수 없음
    # print_tree(lazy[fr], LEAF_CNT)
    for c in range(2):
        if lazy[to][node_idx+c] != -1:
            propagate(to, node_idx+c)
    for num in range(10):
        for c in range(2):
            if lazy[num][node_idx+c] == fr: 
                lazy[num][node_idx+c] = to
    
    for c in range(2):
        if lazy[fr][node_idx+c] == -1:
            lazy[fr][node_idx+c] = to
    

def propagate(fr, node_idx):
    if (to :=lazy[fr][node_idx]) != -1:
        # print(fr)
        # print_tree(lazy[fr], LEAF_CNT)
        segtree[to][node_idx] = (segtree[to][node_idx] + segtree[fr][node_idx])%MOD
        segtree[fr][node_idx] = 0
        lazy[fr][node_idx] = -1
        if node_idx < FIRST_LEAF:
            serialization(fr, to, node_idx*2)

def sub_query(num, i, j, node_idx, l, r):
    if num==0:
        propagate_all(node_idx)

    if r < i or j < l : # 전혀 겹치지 않는 경우
        return 0

    if i <= l and r <= j: # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우
        return segtree[num][node_idx]
    
    elif node_idx < FIRST_LEAF:
        m= l+r>>1

        lquery = sub_query(num, i,j, node_idx*2, l, m)
        rquery = sub_query(num, i,j, node_idx*2+1, m+1, r )
        # print(lquery, rquery)
        return (lquery * mod_arr[min(r,j)-m] + rquery)%MOD
    
    else: #여기서 else는 뭔가 잘못된 거
        assert(0)
    
def print_tree(tree,leaf_cnt):
    return
    level=1
    while level<=leaf_cnt:
        print(tree[level:level*2])
        level<<=1


def propagate_all(node_idx):
    for num in range(10):
        propagate(num, node_idx)


def sub_update(i,j, node_idx, l,r, fr, to):

    propagate_all(node_idx)
    
    if r < i or j < l : # 전혀 겹치지 않는 경우
        pass

    elif i <= l and r <= j: # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우
        # print(l,r,fr,to)
        lazy[fr][node_idx] = to
        propagate(fr, node_idx)
    
    elif node_idx < FIRST_LEAF:
        m= l+r>>1
        lnode_idx = node_idx*2
        rnode_idx = lnode_idx+1
        sub_update(i,j, lnode_idx, l,m, fr, to)
        sub_update(i,j, rnode_idx, m+1,r, fr,to)
        segtree[fr][node_idx]= (segtree[fr][lnode_idx] * mod_arr[r-m] + segtree[fr][rnode_idx])%MOD
        segtree[to][node_idx]= (segtree[to][lnode_idx] * mod_arr[r-m] + segtree[to][rnode_idx])%MOD
        
    else: #여기서 else는 뭔가 잘못된 거
        assert(0)


def update(i,j,fr,to):
    sub_update(i+OFFSET,j+OFFSET,1, 0, LEAF_CNT-1,fr,to)

def query(i,j):

    remainder = 0
    for num in range(1,10):
        remainder = (remainder+sub_query(num, i, j, 1, 0, LEAF_CNT-1)*num) %MOD

    return remainder



for num in range(10):
    init(num, 1,0,LEAF_CNT-1)

# for num in range(10):
#     print(segtree[num])
for _ in range(Q):
    # c, *x = '2 1 100000'.split()
    c,*x = read().split()
    if c == '1':
        i,j,fr,to = map(int, x)
        if fr == to: #fr =to는 그냥 걸러버리자
            continue
        update(i,j,fr,to)
        # for num in range(10):
            # print(segtree[num])
        # print(8)
        # print_tree(lazy[8], LEAF_CNT)
        # print_tree(segtree[8], LEAF_CNT)
        # print(5)
        # print_tree(lazy[5], LEAF_CNT)
        # print_tree(segtree[5], LEAF_CNT)
       

    elif c== '2':
        
        i,j = map(int,x)
        print(query(i+OFFSET,j+OFFSET))
    
