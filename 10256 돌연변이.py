import sys,copy
from collections import deque
try:
    read = open('stdout.txt', 'r').readline
except:
    read = sys.stdin.readline

class Node():

    def __init__(self):
        #인스턴스변수 생성
        self.isend = False
        self.fail = None
        self.child = [None]*4

class Trie():
    def __init__(self):
        #인스턴스변수 생성
        self.root = Node()
        self.root.fail = self.root
    def insert(self,s):
        curnode = self.root
        for c in s:
            if curnode.child[c] is None:
                curnode.child[c] = Node()
            curnode = curnode.child[c]
        curnode.isend = True

    def failure(self):
        q = deque([self.root])
        while q: #bfs
            curnode = q.popleft()

            for c in range(4):
                nextnode = curnode.child[c]
                if nextnode is None:
                    continue
                #curnode 가 root인경우에 예외처리하지않으면 child들의 fail이 자기자신이돼버림 그러면 안됨
                if curnode == self.root:
                    nextnode.fail= self.root
                else:
                    fail = curnode.fail
                    while fail!=self.root and fail.child[c] is None:
                        # curnode의 fail을 계속타고올라가되 fail들에서 c로 갈 수 있는지를봄
                        # c로 갈 수 있는 fail 중 가장 깊은 것의 c노드가 바로 nextnode의 fail이된다.
                        fail = fail.fail

                    if fail.child[c] is not None:
                        nextnode.fail = fail.child[c]
                    else:
                        nextnode.fail = fail
                if nextnode.fail.isend: #이게 중요함! 한 단어가 다른 단어에 포함된 경우 똑같이 단어의 끝으로 생각해야함.
                    nextnode.isend = True
                q.append(nextnode)


    def kmp(self, s):
        curnode = self.root
        cnt=0
        for c in s:
            while curnode != self.root and curnode.child[c] is None:
                #print(curnode.child,c,curnode.fail, self.root)
                #failure함수와 매우유사하다. fail을 타고 계속올라가되 c로 갈 수 있으면 break
                curnode = curnode.fail
            if curnode.child[c] is not None:
                #c로 갈 수 있으면 가고 아니면 root이므로 가만히 있음.
                curnode = curnode.child[c]
            if curnode.isend:
                cnt+=1
        return cnt


for _ in range(int(read())):
    n,m  = map(int,read().split())

    t=Trie()
    dna= read().strip()
    dna = [['A','G','C','T'].index(c) for c in dna] #dict를 사용하지 않기 위해 a,g,c,t를 0,1,2,3으로 변환후 child를 리스트 자료형 으로 바꿔준다!
    marker= read().strip()
    marker = [['A','G','C','T'].index(c) for c in marker]
    for s in range(m - 1):  # 두번째 부분의 s는 0~m-2까지 될수 있고 e는 s+1~m-1까지 될수있다
        for e in range(s + 1, m):
            mutant = copy.deepcopy(marker)
            for i in range(e-s+1): #s가 0 e가 1라면 길이는 2
                mutant[s+i] = marker[e-i]
            t.insert(mutant)
    t.insert(marker)
    t.failure()
    ans=t.kmp(dna)
    print(ans)

