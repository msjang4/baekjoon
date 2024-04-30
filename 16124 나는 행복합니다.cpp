/*input
5886899678
7
2 6 9
1 2 9 8 5
1 1 3 5 0
2 1 6
1 1 10 0 2
1 5 8 8 1
2 1 10
*/
#include <iostream>
#include <stdio.h>
#include <string>
#include <cassert>
#include <memory.h>
using namespace std;
long long MOD = 998244353;
const int MAX_TREE_SIZE=1024*1024*2;
const int MAX_N =1000000;
long long segtree[MAX_TREE_SIZE][10]={0,};
int lazy[MAX_TREE_SIZE][10];
long long ret[MAX_TREE_SIZE][10] ={0,};
long long mod_arr[MAX_N];
int Q,N, FIRST_LEAF=1,LEAF_CNT, OFFSET, LOG=1, TREE_SIZE;


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
    //전파할때 tmp에 한번담는 이유는 3->5, 2->3같은게 순서 상관없이 동작해야돼서 
    int lnode_idx=node_idx*2, to;
    for (int fr=0;fr<10;fr++){
        if ((to =lazy[node_idx][fr]) != -1){
            tmp[to] = (tmp[to] + segtree[node_idx][fr])%MOD;
        } else{
            tmp[fr] = (tmp[fr] + segtree[node_idx][fr])%MOD;
        }
    }  

    int* parent_map = lazy[node_idx];
    for (int num=0;num<10;num++){
        segtree[node_idx][num] = tmp[num];
            
        if (node_idx < FIRST_LEAF){
            for(int c =0;c<2;c++){
                //부모가 1->2를 가지고 있으면
                // 자식의 3->1은 3->2가돼야해서 두번매핑시킴
                // 여기서 num이 3, child_map[3] = 1, parent_map[1] = 2가 될거임

                //여기서 두가지 경우를 더 생각해야함.
                // 첫째 child_map[x]가 -1인경우 -> parent_map[x]로 덮어씌움.
                // 둘째 child_map[x]는 y인데 parent_map[y]가 -1인 경우 그대로 둔다.
                int* child_map = lazy[lnode_idx+c];
                if (child_map[num] == -1){
                    child_map[num] = parent_map[num];
                }
                else if(parent_map[child_map[num]]!=-1){
                    child_map[num]= parent_map[child_map[num]];
                }
            }
        }
    }
    for(int num=0;num<10;num++){
        lazy[node_idx][num] = -1;
    }
}
long long none_arr [10] = {0,};
long long* sub_query( int i, int j, int node_idx, int l, int r){
    
    propagate_all(node_idx);

    if (r < i || j < l){// # 전혀 겹치지 않는 경우
        return none_arr;
    }
    if (i <= l && r <= j){// # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우{
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
        for(int num=0;num<10;num++){
            ret[node_idx][num] = (lquery[num]*mod_arr[min(r,j)-m] + rquery[num])%MOD;
        }
        // cout << endl;
        return ret[node_idx];
    }
    else {//#여기서 else는 뭔가 잘못된 거
        assert(0);
    } 
}
void sub_update(int i,int j, int node_idx, int l,int r, int fr, int to){

    propagate_all(node_idx);
    
    if (r < i || j < l){ //# 전혀 겹치지 않는 경우
     //   pass
    }

    else if (i <= l && r <= j){// # [i,j] 구간내에 [l,r]구간이 완전히 속하는 경우
        lazy[node_idx][fr] = to;
        propagate(fr, node_idx);
    }
    else if (node_idx < FIRST_LEAF){
        int m= (l+r)>>1;
        int lnode_idx = node_idx*2;
        int rnode_idx = lnode_idx+1;
        sub_update(i,j, lnode_idx, l,m, fr, to);
        sub_update(i,j, rnode_idx, m+1,r, fr,to);
        
        segtree[node_idx][fr]= (segtree[lnode_idx][fr] * mod_arr[r-m] + segtree[rnode_idx][fr])%MOD;
        segtree[node_idx][to]= (segtree[lnode_idx][to] * mod_arr[r-m] + segtree[rnode_idx][to])%MOD;
    }else{ //#여기서 else는 뭔가 잘못된 거
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
    while(Q-->0){
        
        int c,i,j,fr,to;
        cin >> c;
        if (c == 1){
            cin >> i >> j >> fr >> to;
            if (fr == to)// #fr =to는 그냥 걸러버리자
                continue;
            update(i,j,fr,to);
        }
        

        else if (c== 2){
            cin >> i >> j;
            cout << query(i+OFFSET,j+OFFSET) << "\n";
    
        }
    }
 }   
int main(void){
    memset(lazy, -1, sizeof(lazy));
    ios::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);
    string S;
    cin>>S;
    N= S.length();
    cin >> Q;

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