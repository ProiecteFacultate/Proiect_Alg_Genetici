#include <iostream>
#include <vector>

using namespace std;

int main()
{
    int n, K, sum = 0;
    cin >> n >> K;
    vector<int> S(n);

    for (int i = 0; i < n; i++)
        cin >> S[i];

    for (int i = 0; i < n; i++)
        if(S[i] >= K / 2)
            sum = S[i];
        else if (sum + S[i] <= K)
            sum += S[i];

    cout << sum << endl;

    return 0;
}
