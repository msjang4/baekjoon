    package hard;

    import java.io.BufferedReader;
    import java.io.IOException;
    import java.io.InputStreamReader;
    import java.math.BigInteger;

    public class _5615 {
        public static void main(String[] args) throws IOException {
            // (2xy+x+y)*2 +1 = (2x+1) (2y+1)


            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

            int n = Integer.parseInt(br.readLine());
            int answer = 0;
            while(n-->0){
                if(isPrime(Long.parseLong(br.readLine())*2+1)){
                    answer++;
                }
            }
            System.out.println(answer);
        }
        static int[] testA = new int[] {2,7,61};
        static boolean isPrime(long n){
            long d=n-1, s=0;
            while(d%2==0){
                d>>=1;
                s++;
            }
            for (int a: testA){
                if(a==n){
                    return true;
                }
                if (a<n && !millerLabinTest(a,d,s,n)) {
                    return false;
                }
            }
            return true;
        }

        static boolean millerLabinTest(int a, long d,long s, long n){
            BigInteger r= modpow(BigInteger.valueOf(a),d,BigInteger.valueOf(n));

            if (r.equals(BigInteger.ONE)) {
                return true;
            }
            while(s-->0){
                if (r.longValue() == n-1){
                    return true;
                }
                r= r.multiply(r).mod(BigInteger.valueOf(n));
            }
            return false;

        }

        static BigInteger modpow(BigInteger b, long s, BigInteger n){
            if(s==0){
                return BigInteger.ONE;
            }else if(s==1){
                return b.mod(n);
            }
            BigInteger m = modpow(b, s/2, n);
            return m.multiply(m).mod(n).multiply(modpow(b,s%2,n)).mod(n);
        }
    }
