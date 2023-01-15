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
MAX= 1_000_000

a = [0]+[1]*(MAX+1)
b= [0]*(MAX+1)
for i in range(2,MAX//2):
    if a[i]:
        b[i*2] = 1
        if i <= MAX**0.5: #루트N 이하인경우에만
            for j in range(2*i,MAX+1,i):
                a[j] = 0
a[1] = 0
a[2] = 0 #a는 홀수소수리스트여야함.
n= int(read())
c=multifly(a,b)

for _ in range(n):
    print(c[int(read())])
#t랑 b를 60000차수의 다항식으로 생각하여 곱하면 12만차수의 다항식의 계수가 나옴.
#n차항의 계수가 c_n일때  n에 6만을 빼고 나누기를 한 값이 x면, 중간 구멍 x좌표를 통해 만들수있는 바늘통과 경우의수가 c_n임.
