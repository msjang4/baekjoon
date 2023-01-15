import sys
from math import pi,log2,ceil,sin, cos

try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

sys.setrecursionlimit(10**5)

def fft(a,w):
    n= len(a)
    if n==1:
        return
    even = []
    odd = []
    for i in range(n):
        if i%2:
            odd.append(a[i])
        else:
            even.append(a[i])
    fft(odd,w**2)
    fft(even,w**2)
    wp= 1
    for i in range(n//2): #fft분할원리.png와 fft의 시간복잡도.txt 참고
        a[i] = even[i] + wp*odd[i]
        a[i+n//2] = even[i] - wp*odd[i]
        wp*=w


def multifly(a,b):
    lensum = len(a)+len(b)
    size = 2**ceil(log2(lensum-1)) #왜 size를 이렇게 잡는지는 합성곱과 DFT관계.png참고
    a += [0] * (size - len(a))
    b += [0] * (size - len(b))
    w = complex(cos(2*pi / size),sin(2*pi / size))

    #a는 반시계방향, b는 시계방향으로 돌려서 dft를 한다.
    fft(a,w)
    fft(b,w)
    #서로 반대방향 dft를 곱하면
    c = [a[i]*b[i] for i in range(size)]
    fft(c, 1/w) # w= e^x면 1/w = e^-x임. IDFT의 직관적인 의미.txt 참고

    c= [round((c[i]/size).real) for i in range(size)]
    return c[:lensum]


tn= int(read())
t=[ *map(int,read().split())]
mn = int(read())
m=[*map(int,read().split())]
bn = int(read())
b = [*map(int, read().split())]

ti = [0]*(60000+1)
bi = [0]*(60000+1)
for i in range(tn):
    ti[t[i]+30000] = 1
for i in range(bn):
    bi[b[i]+30000] = 1

#t랑 b를 60000차수의 다항식으로 생각하여 곱하면 12만차수의 다항식의 계수가 나옴.
#n차항의 계수가 c_n일때  n에 6만을 빼고 나누기를 한 값이 x면, 중간 구멍 x좌표를 통해 만들수있는 바늘통과 경우의수가 c_n임.

c=multifly(ti,bi)
ans=0
for i in range(mn):
    ans += c[(m[i] +30000)*2]
print(ans)