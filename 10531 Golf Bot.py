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
    return c
n= int(read())
a=[0]*(200_000+1)
b=[0]*(200_000+1)
a[0] = 1

for i in range(n):
    k = int(read()) #x가 칠수있는 거리일때 x차수 계수가 1이라고 생각하고
    #두 다항식을 곱하면 두번쳐서 v거리를 갈 수 있다면 v차수에 계수가 잇을거고
    # 갈수 없다면 v차수의 계수가 0일것이다!!
    a[k] = 1
    b[k]=1
c= multifly(a,b)
n = int(read())
ans=0
for i in range(n):

    ans+= c[int(read())]>0
print(ans)