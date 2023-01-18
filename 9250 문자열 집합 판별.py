import sys
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
        self.child = {}


class Trie():
    def __init__(self):
        #인스턴스변수 생성
        self.root = Node()
        self.root.fail = self.root
    def insert(self,s):
        curnode = self.root
        for c in s:
            if c not in curnode.child:
                curnode.child[c] = Node()
            curnode = curnode.child[c]
        curnode.isend = True

    def failure(self):
        q = deque([self.root])
        while q: #bfs
            curnode = q.popleft()

            for c in curnode.child:
                nextnode = curnode.child[c]
                #curnode 가 root인경우에 예외처리하지않으면 child들의 fail이 자기자신이돼버림 그러면 안됨
                if curnode == self.root:
                    nextnode.fail= self.root
                else:
                    fail = curnode.fail
                    while fail!=self.root and c not in fail.child:
                        # curnode의 fail을 계속타고올라가되 fail들에서 c로 갈 수 있는지를봄
                        # c로 갈 수 있는 fail 중 가장 깊은 것의 c노드가 바로 nextnode의 fail이된다.
                        fail = fail.fail

                    if c in fail.child:
                        nextnode.fail = fail.child[c]
                    else:
                        nextnode.fail = fail
                if nextnode.fail.isend: #이게 중요함! 한 단어가 다른 단어에 포함된 경우 똑같이 단어의 끝으로 생각해야함.
                    nextnode.isend = True
                q.append(nextnode)


    def kmp(self, s):
        curnode = self.root
        for c in s:
            while curnode != self.root and c not in curnode.child:
                #print(curnode.child,c,curnode.fail, self.root)
                #failure함수와 매우유사하다. fail을 타고 계속올라가되 c로 갈 수 있으면 break
                curnode = curnode.fail
            if c in curnode.child:
                #c로 갈 수 있으면 가고 아니면 root이므로 가만히 있음.
                curnode = curnode.child[c]
            if curnode.isend:
                return True
        return False


t=Trie()
n= int(read())
for _ in range(n):
    t.insert(read().strip())

t.failure()

n = int(read())
for _ in range(n):
    ans=t.kmp(read().strip())
    print( 'YES' if ans else 'NO')

