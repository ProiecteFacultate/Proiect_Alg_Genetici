#include <iostream>
#include <vector>

using namespace std;

//Avand n = numarul de elemtent din S, complexitatea de spatiu est O(nK), pt ca creem o matrice cu n + 1 linii si k + 1 coloane. Complexitatea de timp este aceeasi O(nK) deoarece parcurgem aceasta
//matrice o singura data.
//Dem optim: Problema foloseste programarea dinamica, la fiecare pas alegand o solutie optima partiala, astfel solutia finala fiind cea optima.

int main()
{
    int n, K;
    cin >> n >> K;
    vector<int> S(n + 1);
    vector<vector<int>> dp(n + 1, vector<int>(K + 1, 0));

    for(int i = 1; i <= n; i++)
        cin >> S[i];

    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= K; j++)
            if (S[i] <= j)
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - S[i]] + S[i]);
            else
                dp[i][j] = dp[i - 1][j];

    cout << dp[n][K];  //suma maxima
}
