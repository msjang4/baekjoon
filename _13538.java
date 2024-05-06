package hard;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.StringTokenizer;

public class _13538 {

    static ArrayList<Node> nodes = new ArrayList<>(Arrays.asList(null, new Node(0,0,0)));


    static int size=0;
    static int X_MAX = 500_000;
    static int LOG = (int)Math.ceil(Math.log(X_MAX)/Math.log(2));
    //세그먼트트리의 리프노드수를 반드시 2의 제곱수로 해야 xor쿼리가 동작함. 아니면 init이 완전이진트리가 되게 바꿔야되는데 까다로움
    static int LEAF_CNT = 1<<LOG;
    static int M_MAX = 500_000;
    static int[] root = new int[M_MAX+1];
    static StringTokenizer st;
    static class Node{
        int l,r,v;

        public Node(int l, int r, int v) {
            this.l = l;
            this.r = r;
            this.v = v;
        }
    }
    static void init(int nodeIdx, int l, int r){
        if(l==r)
            return;
        int m= (l+r)>>1;
        Node node = nodes.get(nodeIdx);
        node.l = addNode(0,0,0);
        init(node.l, l,m);
        node.r = addNode(0,0,0);
        init(node.r, m+1,r);

    }
    static int xorQuery(int nodeIdx, int diffNodeIdx, int x, int l, int r){

        if (l==r){
            return l;
        }
        Node node = nodes.get(nodeIdx);
        Node diffNode = nodes.get(diffNodeIdx);
        int lv = nodes.get(node.l).v - nodes.get(diffNode.l).v;
        int rv = nodes.get(node.r).v  - nodes.get(diffNode.r).v;
        
        int m= (l+r)>>1;
        boolean bit = (x & (m-l+1))!=0; // m-l+1 = left child의 leaf cnt가 1<<i이기 때문
//        System.out.println("m-l+1 = " + (m-l+1));
//        System.out.println("bit = " + bit);
        if ( rv ==0 || ( bit && lv != 0 )){ // rv가 0이거나 i번 비트가 1이면 최댓값은 left에 있으나 lv가 0이면 쩔수없이 right로 가야함
            return xorQuery(node.l, diffNode.l, x,l,m);
        } else {
            return xorQuery(node.r, diffNode.r, x,m+1,r);
        }

    }
    static int kthQuery(int nodeIdx, int diffNodeIdx, int k, int l, int r ){

        if (l==r){
            return l;
        }
        Node node = nodes.get(nodeIdx);
        Node diffNode = nodes.get(diffNodeIdx);
        int lv = nodes.get(node.l).v - nodes.get(diffNode.l).v;

        int m= (l+r)>>1;
        if ( k<= lv){
            return kthQuery(node.l, diffNode.l, k,l,m);
        } else {
            return kthQuery(node.r, diffNode.r, k-lv, m+1,r);
        }

    }
    static int query(int nodeIdx, int b, int e, int l, int r){

        if (r < b || e < l){
            return 0;
        }
        Node node = nodes.get(nodeIdx);
        if (b<=l && r <=e){
            return node.v;
        }

        int m= (l+r)>>1;
        return query(node.l, b,e, l,m) + query(node.r, b,e, m+1,r);
    };
    static void update( int x,int d, int nodeIdx,int l, int r){
        if (l==r){
            return;
        }

        int m = (l+r)>>1;
        Node node = nodes.get(nodeIdx);
        if (x <= m){
            Node lnode = nodes.get(node.l);
            node.l = addNode(lnode.l, lnode.r, lnode.v+d);
            update(x,d, node.l, l,m);
        }else{
            Node rnode = nodes.get(node.r);
            node.r = addNode(rnode.l, rnode.r, rnode.v+d);
            update(x,d, node.r, m+1,r);
        }
    }

    public static void main(String[] args) throws IOException {

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        st = new StringTokenizer(br.readLine());
        init(1, 0, LEAF_CNT-1);
        root[0] = 1;
        StringBuilder sb = new StringBuilder();
        int M= nextInt();
        while(M-->0){
            st= new StringTokenizer(br.readLine());
            int queryCode = nextInt();
            int x,l,r,k;
            switch(queryCode){
                case 1:
                    x= nextInt();
                    append(x);
                    break;
                case 2:
                    l= nextInt(); r = nextInt(); x = nextInt();
                    sb.append(xorQuery(root[r],root[l-1],x, 0,LEAF_CNT-1));
                    sb.append("\n");
                    break;
                case 3:
                    k= nextInt();
                    size -=k;
                    break;
                case 4:
                    l= nextInt(); r = nextInt(); x = nextInt();
                    sb.append(query(root[r],1,x,0, LEAF_CNT-1)- query(root[l-1],1,x,0,LEAF_CNT-1));
                    sb.append("\n");
                    break;
                case 5:
                    l= nextInt(); r = nextInt(); k = nextInt();
                    sb.append(kthQuery(root[r], root[l-1], k, 0, LEAF_CNT-1));
                    sb.append("\n");

                    break;
            }
        }
        System.out.print(sb);
    }
    static void append(int x){

        Node preRoot= nodes.get(root[size]);
        root[++size] = addNode(preRoot.l, preRoot.r, preRoot.v+1);
        update(x, 1, root[size] , 0,LEAF_CNT-1);

    }

    static int addNode(int l, int r, int v){
        nodes.add(new Node(l,r,v));
        return nodes.size()-1;
    }
    static int nextInt(){
        return Integer.parseInt(st.nextToken());
    }
}
