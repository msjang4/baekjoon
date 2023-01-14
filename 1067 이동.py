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
n= int(read())
a=[*map(int,read().split())]
b=[*map(int,read().split())]
#n차 다항식끼리 곱한 것의 m차항은 j+k=m 인 a_jb_k의 합인데
#여기서 b를 리버스시킨다면 a_jb_n-k의 합이되며 n-k-j = n-m으로 a항과 b항의 인덱스차가 동일해진다.
#n>=m인경우는 (j+(n-m))%(n+1)==k인 a_jb_k의합이다.
#n<m인경우는 (n+1+j+(n-m))%(n+1)==k인 a_jb_k의합이다.
#즉 n>=i인 , i차식은 b항들이 a항보다 (n-i)만큼 인덱스 차가 나며
# i+n+1차식도  n+j+(n-i-n-1) = j+(n-i)이므로 동일하다.
# 따라서 c[i] + c[i+n+1] = a_j b_j+(n-i)의 합이다.
#코드상에서는 n이 차수+1이므로 c[i]+c[i+n]으로 하면됨.

b.reverse()

c=multifly(a,b)
ans=c[n-1]
for i in range(n-1):
    ans = max(c[i]+c[i+n],ans)
print(ans)