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
        self.child = 0 # 5000*5000*26을 메모리가 넘많이먹음 bitmask를 이용해 5000*5000으로 줄인다!
        self.childs = []




class Trie():
    def __init__(self):
        #인스턴스변수 생성
        self.root = Node()
        self.root.fail = self.root
    def insert(self,s):
        curnode = self.root
        for c in s:
            c = ord(c)-ord('a')
            if not (1 << c) & curnode.child:
                curnode.child |= (1<<c)
                curnode.childs.append((c,Node()))
            for i,node in curnode.childs:
                if c==i:
                    curnode = node
                    break
        curnode.isend = len(s)
    #5000 x 5000으로 구한다
    # fail은 근데 25000000 이고, 26, 아니지
    def failure(self):
        q = deque([self.root])
        while q: #bfs
            curnode = q.popleft()

            for c,nextnode in curnode.childs:
                #curnode 가 root인경우에 예외처리하지않으면 child들의 fail이 자기자신이돼버림 그러면 안됨
                if curnode == self.root:
                    nextnode.fail= self.root
                else:
                    fail = curnode.fail
                    while fail!=self.root and not (1<<c) & fail.child:
                        # curnode의 fail을 계속타고올라가되 fail들에서 c로 갈 수 있는지를봄
                        # c로 갈 수 있는 fail 중 가장 깊은 것의 c노드가 바로 nextnode의 fail이된다.
                        fail = fail.fail

                    if (1<<c) & fail.child:

                        for i, node in fail.childs:
                            if c == i:
                                nextnode.fail = node
                                break
                    else:
                        nextnode.fail = fail
                #nextnode가 끝이 아닌경우에
                if not nextnode.isend: #이게 중요함! 한 단어가 다른 단어에 포함된 경우 똑같이 단어의 끝으로 생각해야함.
                    nextnode.isend = nextnode.fail.isend

                q.append(nextnode)


    def kmp(self, s):
        curnode = self.root
        li=[]
        for idx,c in enumerate(s,start=1):
            c = ord(c)-ord('a')
            while curnode != self.root and not (1<<c) & curnode.child:
                #print(curnode.child,c,curnode.fail, self.root)
                #failure함수와 매우유사하다. fail을 타고 계속올라가되 c로 갈 수 있으면 break
                curnode = curnode.fail
            if (1<<c) & curnode.child:
                #c로 갈 수 있으면 가고 아니면 root이므로 가만히 있음.

                for i, node in curnode.childs:
                    if c == i:
                        curnode = node
                        break
            if curnode.isend:
                li.append((idx-curnode.isend,idx)) #아스키 타일 구간을 리스트로 만듦

        li.sort()
        ans = 0
        idx=0

        for x in li: #수직선에 겹치는 구간 구하는 알고리즘쓰면됨.
            l,r = x
            if idx < r:
                ans+=r-max(idx,l)
                idx = r
        return ans





n= int(read())
s= read().strip()
t=Trie()
m = int(read())
for _ in range(m):
    t.insert(read().strip())
t.failure()
print(n-t.kmp(s))

