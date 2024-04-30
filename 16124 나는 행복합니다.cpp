/*input
0123456789
4
1 3 10 4 6
1 3 10 9 4
1 3 10 3 9
2 4 5
*/
// import sys
// import math
// read = sys.stdin.readline
// # print = sys.stdout.write
// S = read().strip()
// # S = '1234567890'*(10**5)
// N = len(S)
// LOG = math.ceil(math.log2(N))
// FIRST_LEAF = LEAF_CNT= 2**LOG
// OFFSET = LEAF_CNT-N-1
// mod_arr = [1]*(10**6)
#include <iostream>
#include <stdio.h>
#include <string>
#include <cassert>
#include <random>
#include <memory.h>
using namespace std;
long long MOD = 998244353;
const int MAX_TREE_SIZE=1024*1024*2;
const int MAX_N =10;//00000;
long long segtree[MAX_TREE_SIZE][10]={0,};
int lazy[MAX_TREE_SIZE][10];
long long ret[MAX_TREE_SIZE][10] ={0,};
long long mod_arr[MAX_N];
int Q,N, FIRST_LEAF=1,LEAF_CNT, OFFSET, LOG=1, TREE_SIZE;
bool debug = false;
// long long segtree[][2**(LOG+1)] = [[0]*(2**(LOG+1)) for _ in range(10)]
// lazy = [[-1]*(2**(LOG+1)) for _ in range(10)]

long long* init( int node_idx, int l,int r){
    if (node_idx < FIRST_LEAF){
        int m=( l+r)>>1;
        long long* lnode = init(node_idx*2,l,m);
        long long*  rnode= init(node_idx*2+1, m+1,r);
        for (int num=0;num<10;num++)
            segtree[node_idx][num] = (lnode[num]*mod_arr[r-m] + rnode[num]) %MOD;
    }
    
    

    return segtree[node_idx];
}
        


void propagate(int fr, int node_idx);
void serialization(int fr, int to, int node_idx){
    // # 행동들이 실행되는 순서에 상관없도록 직렬화를 시켜준다.
    // # print_tree(lazy[fr], LEAF_CNT)
    for(int c =0;c<2;c++){

    // # 즉 fr->to 변경시 0~9중에 fr로 바뀌는게 있다면 그 행동을 to로 바뀌는걸로 취급
        for (int num=0;num<10;num++)
            if (lazy[node_idx+c][num] == fr)
                lazy[node_idx+c][num] = to;

    // # 이미 fr이 무언가로 바뀐다면 덮어씌울 수 없음
        if (lazy[node_idx+c][fr] == -1)
            lazy[node_idx+c][fr] = to;
    }
}

void propagate(int fr, int node_idx){
    int to;
    if ((to =lazy[node_idx][fr]) != -1){
        // # print(fr)
        // # print_tree(lazy[fr], LEAF_CNT)
        segtree[node_idx][to] = (segtree[node_idx][to] + segtree[node_idx][fr])%MOD;
        segtree[node_idx][fr] = 0;
        lazy[node_idx][fr] = -1;
        if (node_idx < FIRST_LEAF)
            serialization(fr, to, node_idx*2);
    }
}

void propagate_all(int node_idx){
    long long tmp[10]={0,};
    long long lazy_tmp[2][10];
    memset(lazy_tmp,-1, sizeof(lazy_tmp));
    //전파할때 tmp에 한번담는 이유는 3->5, 2->3같은게 순서 상관없이 동작해야돼서 

    for (int fr=0;fr<10;fr++){
        int to;
        if ((to =lazy[node_idx][fr]) != -1){
        // # print(fr)
        // # print_tree(lazy[fr], LEAF_CNT)
            lazy[node_idx][fr] = -1;
            tmp[to] = (tmp[to] + segtree[node_idx][fr])%MOD;
            if (node_idx < FIRST_LEAF){
                int lnode_idx = node_idx*2;

                for(int c =0;c<2;c++){
                    // # 즉 fr->to 변경시 0~9중에 fr로 바뀌는게 있다면 그 행동을 to로 바뀌는걸로 취급
                    for (int num=0;num<10;num++)
                        if (lazy[lnode_idx+c][num] == fr)
                            lazy_tmp[c][num] = to;

                    // # 이미 fr이 무언가로 바뀐다면 덮어씌울 수 없음
                    if (lazy[lnode_idx+c][fr] == -1)
                        lazy_tmp[c][fr] = to;
                }
            }
        } else{

            tmp[fr] = (tmp[fr] + segtree[node_idx][fr])%MOD;
            
        }
    }  
    for (int num=0;num<10;num++){
        segtree[node_idx][num] = tmp[num];
            
        
        if (node_idx < FIRST_LEAF){
            int lnode_idx=node_idx*2;
            for(int c =0;c<2;c++){
                lazy[lnode_idx+c][num]=lazy_tmp[c][num]==-1?lazy[lnode_idx+c][num] :lazy_tmp[c][num] ; 
            }
        }
    }

}
long long none_arr [10] = {0,};
long long* sub_query( int i, int j, int node_idx, int l, int r){
    
    propagate_all(node_idx);

    if (r < i || j < l){// # 전혀 겹치지 않는 경우
        // cout << "none: " << l << ", " << r << endl;
        return none_arr;
    }
    if (i <= l && r <= j){// # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우{
        // cout << "contain: " << l << ", " << r << endl;
        return segtree[node_idx];

    }
    
    else if (node_idx < FIRST_LEAF){
        int m= (l+r)>>1;
        if (j <= m){
            return sub_query(i,j,node_idx*2,l,m);
        }
        if (m< i){
            return sub_query(i,j,node_idx*2+1,m+1,r);
        }

        long long* lquery = sub_query(i,j, node_idx*2, l, m);
        long long* rquery = sub_query(i,j, node_idx*2+1, m+1, r );
        //# print(lquery, rquery)
        // cout << l << ", "  << r << ", "<<  min(r,j) -m << endl;
        for(int num=0;num<10;num++){
            ret[node_idx][num] = (lquery[num]*mod_arr[min(r,j)-m] + rquery[num])%MOD;

                // cout << min(r,j)-m<<", " << "[" << lquery[num] << ", " << rquery[num] <<", " << ret[node_idx][num] << "], " ;
            
        }
        // cout << endl;
        return ret[node_idx];
    }
    else {//#여기서 else는 뭔가 잘못된 거
        assert(0);
    } 
}
void print_tree(void * arr,int tree_size,int num, bool is_lazy){
    int level=1;
    while (level<tree_size){
        cout << "level " << level << ": [";
        for(int i=level;i<level*2;i++){
            if (is_lazy){
                int (* tree)[10] = (int (*)[10]) arr;
                cout << tree[i][num] << ", ";

            }else{

                long long (* tree)[10] = (long long (*)[10]) arr;
                cout << tree[i][num] << ", ";
            }
        }
        cout << "]" << endl;
        level<<=1;
    }
}

void sub_update(int i,int j, int node_idx, int l,int r, int fr, int to){

    propagate_all(node_idx);
    
    if (r < i || j < l){ //# 전혀 겹치지 않는 경우
     //   pass
    }

    else if (i <= l && r <= j){// # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우
        //# print(l,r,fr,to)
        lazy[node_idx][fr] = to;
        propagate(fr, node_idx);
    }
    else if (node_idx < FIRST_LEAF){
        int m= (l+r)>>1;
        int lnode_idx = node_idx*2;
        int rnode_idx = lnode_idx+1;
        sub_update(i,j, lnode_idx, l,m, fr, to);
        sub_update(i,j, rnode_idx, m+1,r, fr,to);
        for (int num=0;num<10;num++){
            segtree[node_idx][num]= (segtree[lnode_idx][num] * mod_arr[r-m] + segtree[rnode_idx][num])%MOD;
 
        }
        }
    else{ //#여기서 else는 뭔가 잘못된 거
        assert(0);
    }
    }

void update(int i,int j,int fr,int to){
    sub_update(i+OFFSET,j+OFFSET,1, 0, LEAF_CNT-1,fr,to);
}
long long query(int i,int j){

    long long remainder = 0;
    long long * r_arr = sub_query( i, j, 1, 0, LEAF_CNT-1);
    for (int num=0;num<10;num++)
        remainder = (remainder+r_arr[num]*num) %MOD;

    return remainder;
}

 void solve(){
    for (int num=0;num<10;num++){
        init( 1,0,LEAF_CNT-1);
    }
    random_device rd; 
    mt19937 mt(rd()); 
    uniform_int_distribution<int> dist(1, MAX_N); 
    uniform_int_distribution<int> dist2(0, 9); 
    if(debug){
        Q=20;
    }
    while(Q-->0){
        
        int c,i,j,fr,to;
        if(debug){  
            c=Q>=2?1:2;i=dist(mt);j=dist(mt);
            if (i>j){
                long long tmp;
                tmp=i;
                i=j;
                j=tmp;
            }
            if (c==1){
                fr=dist2(mt);to=dist2(mt);
            printf("%d %d %d %d %d\n",c,i,j,fr,to);
            }else{

            printf("%d %d %d\n",c,i,j);

            }
        }
        else
            scanf("%d\n", &c);
        if (c == 1){
            if(!debug)
                scanf("%d %d %d %d\n", &i,&j,&fr,&to);
            if (fr == to)// #fr =to는 그냥 걸러버리자
                continue;
            update(i,j,fr,to);
        }
        

        else if (c== 2){
            if(!debug)
             scanf("%d %d\n", &i,&j);
            printf("%lld\n",query(i+OFFSET,j+OFFSET));
    
        }
        // int d=0;
        // for (int num=3;num<10;num+=d){
        //     d+=1;
        //     cout << "segtree " <<num <<endl;
        //     print_tree(segtree, TREE_SIZE,num, false);
        //     cout << "lazytree " <<num <<endl;
        //     print_tree(lazy, TREE_SIZE,num, true);
        // }
    }
 }   
int main(void){
    memset(lazy, -1, sizeof(lazy));
    string S;
    cin>>S;
    char* repeat= "0123456789";
    if (debug || S[0]=='-' ){

        S = string(MAX_N, '1');
        for(int i=0;i<MAX_N;i++){
            S[i] = repeat[i%10];
        }
    }
    N= S.length();
    scanf("%d\n", &Q);

    while (FIRST_LEAF <= N){
        FIRST_LEAF<<=1;
        LOG+=1;
    }
    LEAF_CNT = FIRST_LEAF;
    OFFSET = LEAF_CNT-N-1;
    TREE_SIZE = FIRST_LEAF+LEAF_CNT;


    for(int i=1; i<= N;i++){
        int num = S[i-1]-'0';
        segtree[FIRST_LEAF+OFFSET+i][num] = 1;
    }
    mod_arr[0] = 1;
    for (int i=1;i<N;i++){
        mod_arr[i] = mod_arr[i-1]*10%MOD;
    }
    solve();

}