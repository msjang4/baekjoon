#include <iostream>
#include <string>
#include <complex>
#include <vector>
using namespace std;

void fft(vector<complex<double>>& a, complex<double> w){
    if(a.size()==1)
        return;
    vector<complex<double>> odd(a.size()/2);
    vector<complex<double>> even(a.size()/2);
    for(int i=0;i<a.size();i++){
        if(i%2==0)
            even[i/2] = a[i];
        else
            odd[i/2] = a[i];
    }

    fft(odd,w*w);
    fft(even,w*w);

    complex<double> wp(1,0);
    for(int i=0;i<a.size()/2;i++){
        a[i]= even[i]+ wp*odd[i]; 
        a[i+a.size()/2]=even[i] - wp*odd[i];
        wp*=w;
    }

}
vector<int> multifly(vector<int>& a, vector<int>& b){
    
    int sum = a.size()+b.size()-1;
    int size = pow(2,ceil(log2(sum)));
    vector<complex<double>> ca(size);
    vector<complex<double>> cb(size);

    for(int i=0;i<a.size();i++)
        ca[i] = a[i];
    for (int i=0;i<b.size();i++)
        cb[i] = b[i];
    
    complex<double> w( cos(2*M_PI/size),sin(2*M_PI/size));
 
    fft(ca,w);
    fft(cb,w);

    vector<complex<double>> cc(size);

    for(int i=0;i<size;i++){
        cc[i] = ca[i]*cb[i];
    }
    fft(cc,pow(w,-1));

    vector<int> c(sum);
    for (int i=0;i<c.size();i++){
        c[i] = round(cc[i].real()/size);
    }


    return c;
    
}
int main(){

    string str;
    getline(cin, str, ' ');
    vector<int> a(str.length());
    for (int i=0;i<str.length();i++){
        a[i] = str[i]-'0';
    }
    getline(cin, str);
    vector<int> b(str.length());
    for (int i=0;i<str.length();i++){
        b[i] = str[i]-'0';
    }
    auto c = multifly(a,b);

    for(int i=c.size()-1; i>0;i--){
        
        c[i-1] += c[i]/10;
        c[i] = c[i]%10;
    }
    for(int i=0;i<c.size();i++){
        cout<<c[i];
    }
    cout<<endl;
}   