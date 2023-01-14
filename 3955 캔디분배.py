import sys
from math import ceil
from bisect import bisect_left
from collections import deque
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

sys.setrecursionlimit(10**5)

def extended_euclid(a,b): #가능한 자연수 t1을 리턴함. 불가능한경우 0을 리턴
    if b==1: #b가1이면 s1=0이 되므로 a+1을 리턴하는 예외처리해줌.
        return a+1
    r1,s1,t1 = a,1,0
    r2,s2,t2 = b,0,1
    while r2:
        q = r1//r2
        r1,s1,t1,r2,s2,t2 = r2,s2,t2, r1%r2,s1-q*s2,t1-q*t2
    if r1 != 1:
        return 0
    else:
        if t1 <= 0: #r1이 자연수가 아니면 r2가 0이므로 (s1+s2)*a + (t1+t2)*b가 1이고 t1+t2는 반드시 자연수임.
            return t1+t2
        return t1

t = int(read())
for _ in range(t):
    n,m = map(int,read().split())
    ans= extended_euclid(n,m)
    if ans in range(1,10**9+1):
        print(ans)
    else:
        print('IMPOSSIBLE')
