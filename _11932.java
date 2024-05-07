package hard;
/*
8 5
105 2 9 3 8 5 7 7
1 2
1 3
1 4
3 5
3 6
3 7
4 8
2 5 1
2 5 2
2 5 3
2 5 4
7 8 2
 */
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class _11932 {




    static int N_MAX = 100_000;
    static ArrayList<List<Integer>> adj= new ArrayList<>(N_MAX+1); // 1-indexed
    static int LOG = (int)Math.ceil(Math.log(N_MAX)/Math.log(2));
    static int[][] lcaDp = new int[N_MAX+1][LOG]; // 1-indexed
    static int[] root= new int[N_MAX+1]; // 1-indexed
    static boolean[] visited = new boolean[N_MAX+1]; // 1-indexed
    static int[] w= new int[N_MAX+1]; // 1-indexed
    static int[] sortedW = new int[N_MAX];
    static int[] depth = new int[N_MAX+1];
    static ArrayList<Node> nodes;

    static class Node{
        int l;
        int r;
        int v;

        public Node(int l, int r, int v) {
            this.l = l;
            this.r = r;
            this.v = v;
        }
        static int lv(Node node){
            return nodes.get(node.l).v;
        }

    }
    static void dfs(int u, int parent, int d){

        visited[u] = true;
        Node prev_root = nodes.get(root[parent]);
        root[u] = addNode(prev_root.l, prev_root.r, prev_root.v+1);
        depth[u] = d;
        lcaDp[u][0] = parent;

        int compressedW = Arrays.binarySearch(sortedW, w[u]);
//        System.out.println("compressedW = " + compressedW);
        update(compressedW, 1, root[u], 0,N_MAX-1);
        for(int v : adj.get(u)){
            if (!visited[v]){

                dfs(v,u,d+1);

            }
        }

    }
    static int getLca(int u, int v){
        if (depth[u] < depth[v]){
            int temp = u; u=v; v=temp;
        }
        int i=LOG-1;
        while (depth[u] != depth[v]){
            int parent = lcaDp[u][i];
            if (depth[parent] >= depth[v]){ // u의 2^i번째 parent의 depth가 여전히 v의 depth 이상인지 확인!
                u= parent;
            }
            i--;
        }

        if(u==v){ // depth만 맞췄는데 같은 경우
            return u;
        }

        i=LOG;
        while(i-->0){ // LOG-1 ~ 0
            if (lcaDp[u][i] != lcaDp[v][i]){ // 2^i번째 부모가 다를때만 올라감 , 즉 lca의 자식까지 올라감
                u=lcaDp[u][i];
                v=lcaDp[v][i];
            }
        }

        return lcaDp[u][0];

    }
    static void init(int nodeIdx, int s, int e){

        if (s==e)
            return;
        int m = (s+e)>>1;
        Node node = nodes.get(nodeIdx);
        node.l = addNode(0,0,0);
        init(node.l, s, m);

        node.r = addNode(0,0,0);
        init(node.r, m+1, e);

    }

    static int addNode(int l, int r, int v){
        nodes.add(new Node(l,r,v));
        return nodes.size()-1;
    }
    static void update(int i, int x, int nodeIdx,int l, int r){
        if (l==r){
            return;
        }

        int m = (l+r)>>1;
        Node node = nodes.get(nodeIdx);
        if (i <= m){
            Node lnode = nodes.get(node.l);
            node.l = addNode(lnode.l, lnode.r, lnode.v+x);
            update(i,x, node.l, l,m);
        }else{
            Node rnode = nodes.get(node.r);
            node.r = addNode(rnode.l, rnode.r, rnode.v+x);
            update(i,x, node.r, m+1,r);
        }
    }

    static int operate(int u,int v, int k){ // u -> v경로중 k번째 작은 가중

        int lca = getLca(u,v);
//        System.out.println("lca = " + lca);
        int compressedW = query(root[u],root[v],root[lca],w[lca],k,0,N_MAX-1);
        return sortedW[compressedW];
    }

    static int query(int uNodeIdx, int vNodeIdx, int lcaNodeIdx,int lcaW, int k, int l, int r){

        if(l==r){
            return l;
        }
        Node uNode = nodes.get(uNodeIdx);
        Node vNode = nodes.get(vNodeIdx);
        Node lcaNode = nodes.get(lcaNodeIdx);

        int m= (l+r)>>1;
        int lNodeV = Node.lv(uNode) +Node.lv(vNode) - 2 * Node.lv(lcaNode);
        if (sortedW[l] <= lcaW&&lcaW<=sortedW[m]){ // lca의 가중치가 l번째이상 m번째 이하라면 lNodeV를 1추가해야함.
            lNodeV++;
        }
//        System.out.println("[l,r] = " + sortedW[l]+","+sortedW[r]);
//        System.out.println("lNodeV = " + lNodeV+", k = "+k);
        if(k <= lNodeV){
            return query(uNode.l, vNode.l, lcaNode.l, lcaW,k,l,m);

        }else{
            return query(uNode.r, vNode.r, lcaNode.r, lcaW,k-lNodeV,m+1,r);

        }
    }


    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int N= nextInt(st), M = nextInt(st);

        for(int i=0 ;i<N+1;i++){
            adj.add(new ArrayList<>());
        }

        st = new StringTokenizer(br.readLine());
        for(int i=0;i<N;i++){
            w[i+1] = nextInt(st);
            sortedW[i] = w[i+1];
        }
        Arrays.sort(sortedW);

        for(int i=0;i<N-1;i++){
            st = new StringTokenizer(br.readLine());
            int x = nextInt(st), y = nextInt(st);
            adj.get(x).add(y);
            adj.get(y).add(x);
        }
        nodes = new ArrayList<>(Arrays.asList(null, new Node(0,0,0)));
        init(1, 0, N_MAX-1);
        root[0] = 1;
        dfs(1,0, 1);

        for(int i=1;i<LOG;i++){
            for(int u=1;u<=N;u++){
                lcaDp[u][i] = lcaDp[lcaDp[u][i-1]][i-1];
            }
        }
        StringBuilder sb = new StringBuilder();
        for(int i=0;i<M;i++){
            st = new StringTokenizer(br.readLine());
            int u =nextInt(st), v = nextInt(st), k = nextInt(st);
//            System.out.println(operate(u,v,k));
            sb.append(operate(u,v,k));
            sb.append("\n");
        }
        System.out.print(sb);

    }





    static int nextInt(StringTokenizer st){
        return Integer.parseInt(st.nextToken());
    }

}
