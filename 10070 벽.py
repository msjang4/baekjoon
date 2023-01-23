import sys
from math import ceil, log2

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline
sys.setrecursionlimit(10 ** 2)
n, k = map(int, read().split())
size = 2 ** ceil(log2(n))
default = (-float('inf'), float('inf'))
segtree = [default] * (2 * size)
segtree[size:size + n] = [(0, 0) for i in range(n)]  # 자식노드만 실제값으로 쓸거임.
ans = []
def updateminmax(minmax, op, h):
    _min, _max = minmax
    if op == 1:  # min조정단계
        if h < _min:  # 아무일도 일어나지 않음
            return minmax
        return (h, max(h, _max))
    elif op == 2:
        if h > _max:  # 아무일도 일어나지 않음
            return minmax
        # max값으로 할게 기존 min보다도 작으면 (h,h)를 반환
        return (min(h, _min), h)


def limit_minmax(minmax1, minmax2):  # minmax1을 minmax2로 제한시킴
    if minmax1[1] < minmax2[0]:  # 구간에있는모든 수보다 min값이 더클때
        return (minmax2[0], minmax2[0])
    elif minmax2[1] < minmax1[0]:  # 구간에 있는 모든 수보다 max값이 작을때
        return (minmax2[1], minmax2[1])
    else:
        minval = max(minmax1[0], minmax2[0])
        maxval = min(minmax1[1], minmax2[1])
        return (minval, maxval)


def propagate(i):
    if segtree[i] != default:
        segtree[i * 2] = limit_minmax(segtree[i * 2], segtree[i])
        segtree[i * 2 + 1] = limit_minmax(segtree[i * 2 + 1], segtree[i])
        segtree[i] = default

def dfs(i=1, b=0, e=size-1):
    if i<size:
        m = (b + e) //2
        propagate(i)
        dfs(i*2,b, m)
        dfs(i*2+1, m + 1, e)
    elif i-size<n:
        print(str(segtree[i][0]))

def update(l, r, op, h, i=1, b=0, e=size - 1):
    if i < size:
        # leaf노드는 전파시키지않는다.
        propagate(i)
    if r < b or e < l:
        return
    if l <= b and e <= r:
        if i < size:  # segtree를 전파할건데 구간쿼리가없으므로 자식노드만 해도됨.
            segtree[i * 2] = updateminmax(segtree[i * 2], op, h)
            segtree[i * 2 + 1] = updateminmax(segtree[i * 2 + 1], op, h)
        else:
            segtree[i] = updateminmax(segtree[i], op, h)

    elif i < size:
        m = (b + e) // 2
        update(l, r, op, h, i * 2, b, m)
        update(l, r, op, h, i * 2 + 1, m + 1, e)
    return

# segtree자체가 lazy가되는 좀신기한 형태를 만들게 됐는데
# leafnode가 아닌것들이 다 lazy처럼 사용됨.

for _ in range(k):
    op, l, r, h = map(int, read().split())
    update(l, r, op, h)
dfs()
