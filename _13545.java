package hard;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class _13545 {
    static int[] arr,ansArr, preSum;

    static int sqrtN;
    static class Query implements Comparable<Query>{

        final int l;
        final int r;
        final int idx;
        final int group;

        Query(int l, int r, int idx) {
            this.l = l;
            this.r = r;
            this.idx = idx;
            this.group = l/sqrtN;
        }


        @Override
        public int compareTo(Query o) {
            if (this.group == o.group)
                return this.r - o.r;
            return this.group - o.group;
        }
    }
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = pi(st.nextToken()), k= 100_000*2; // preSum의 원소 k의 범위는 -100_000 ~ 100_000가 됨
        sqrtN = (int)Math.sqrt(n);
        arr = new int[n];
        preSum = new int[n+1];
        st = new StringTokenizer(br.readLine());
        for(int i=0;i<n;i++){
            arr[i] = pi(st.nextToken());
            preSum[i+1] = preSum[i]+arr[i];
        }

        int q = pi(br.readLine());
        List<Query> queryList = new ArrayList<Query>();
        ansArr = new int[q];
        for(int i=0;i<q;i++){
            st = new StringTokenizer(br.readLine());
            int l = pi(st.nextToken())-1;
            int r = pi(st.nextToken());
            queryList.add(new Query(l,r,i));
        }

        Collections.sort(queryList);

        int[] idxMin = null, idxMax=null, idxMaxLGroup=new int[k+1];
        Arrays.fill(idxMaxLGroup, 0);
        int prev_r=0, prev_group=-1, prev_answer=0;

        for(Query query : queryList){
            int l = query.l, r =query.r, group = query.group;
            int groupEnd = (group+1)*sqrtN;

            if (group > prev_group){
                prev_answer =0;
                prev_r = 0;
                idxMin = new int[k+1];
                idxMax = new int[k+1];
                Arrays.fill(idxMin, n);
                Arrays.fill(idxMax, 0);
            }

            for (int i = Math.max(groupEnd,prev_r); i <= r; i++) {
                int idx = getIdx(i);
                idxMin[idx] = Math.min(i,idxMin[idx]);
                idxMax[idx] = Math.max(i,idxMax[idx]);

                prev_answer = Math.max(prev_answer, idxMax[idx]- idxMin[idx]);
            }


            int answer = prev_answer;

            for(int i=Math.min(groupEnd-1,r); i>=l; i--){
                // 한번이라도 arr[i]가 l,r그룹에 들어왔다면 arr[i]의 idxMaxLGroup을 i로 둬도 된다.
                // l이 i이하 이거나 idxMax[arr[i]]가 0이 아닌 경우는 자명함.
                // l이 i보다 크고 idxMax[arr[i]]가 0인 경우에는 음수가 되므로 answer가 변하지 않음
                int idx = getIdx(i);

                idxMaxLGroup[idx] = Math.max(i, idxMaxLGroup[idx]);
                answer = Math.max(Math.max(idxMax[idx],idxMaxLGroup[idx])-i, answer);
            }
            ansArr[query.idx] = answer;
            prev_group = group;
            prev_r = r;

        }

        StringBuilder sb = new StringBuilder();

        for(int ans : ansArr){
            sb.append(ans);
            sb.append("\n");
        }

        System.out.print(sb);

    }
    static int getIdx(int i){
        return preSum[i]+100_000;
    }
    static int pi(String s){
        return Integer.parseInt(s);
    }
}
