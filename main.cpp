#include <stdio.h>
#include <iostream>
#include <random>
#include <vector>
#include <fstream>
using namespace std;

#define N 100  //入力信号の要素数
#define L_max (int) (N * 0.4)
#define TRIAL 10  // 試行回数
#define REPEAT 1000  // 想起を繰り返す回数


int p_or_n(){
    // +1か-1を返す
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> one_two(1, 2);
    return one_two(mt) == 1 ? 1 : -1;
}

int choice(int m){
    // [0, m-1]から1つ選ぶ
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<int> choice(0, m - 1);
    return choice(mt);
}

int signal(double x){
    // x>0なら1, x<0なら-1, x==0なら0を返す
    return x > 0 ? 1 : x < 0 ? -1 : 0;
}

int is_array_same(int *a, int *b){
    // 配列aと配列bの要素が全て一致したら1を返す
    for (int i = 0; i < N; i++){
        if (a[i] != b[i]){
            return 0;
        }
    }
    return 1;
}

double eval_m(int *y, int *ans){
    // 出力信号と正解信号の一致率を計算する
    int sum = 0;
    for (int i = 0; i < N; i++){
        sum += ans[i] * y[i];
    }
    return (double)sum / N;
}

int main(){
    int L, i, j, t, r, n, success, noise_pos;
    double sum, m, acc;
    double w[N][N] = {};
    int ans[N] = {};
    int x[N] = {};
    int y[N] = {};

    // 出力ファイル
    ofstream f("log.txt");
    f << "// N: " << N << ", L_max: " << L_max << ", TRIAL: " << TRIAL << ", REPEAT: " << REPEAT << '\n';

    for (L = 1; L <= L_max; L++){
        // 2次元配列(N×L行列)の動的生成
        vector< vector<int> > e;
        e.resize(L);
        for (i = 0; i < L; i++){
            e[i].resize(N);
        }

        // 記憶パターンの埋め込み
        for (i = 0; i < L; i++){
            for (j = 0; j < N; j++){
                e[i][j] = p_or_n();
            }
        }

        // 記憶パターンから結合係数行列を作成
        for (i = 0; i < N; i++){
            for (j = 0; j < N; j++){
                if (i != j){
                    sum = 0.0;
                    for (r = 0; r < L; r++){
                        sum += e[r][i] * e[r][j];
                    }
                    w[i][j] = (double)sum / N;
                } else {
                    w[i][j] = 0.0;
                }
            }
        }


        // 試行ループ
        success = 0;
        for (t = 0; t < TRIAL; t++){
            r = choice(L);
            noise_pos = choice(N);
            for (i = 0; i < N; i++){
                ans[i] = e[r][i];
                x[i] = e[r][i];
            }
            x[noise_pos] = -x[noise_pos];

            // 想起ループ
            for (n = 0; n < REPEAT; n++){
                // 行列積の計算
                for (i = 0; i < N; i++){
                    sum = 0.0;
                    for (j = 0; j < N; j++){
                        sum += w[i][j] * x[j];
                    }
                    y[i] = signal(sum);
                }

                // xとyが一致したらbreak
                if (is_array_same(x, y))
                    break;

                // 出力yを入力xとしてコピー
                for (i = 0; i < N; i++){
                    x[i] = y[i];
                }
            }
            // 評価
            m = eval_m(y, ans);
            if (m == 1.0)
                success += 1;
        }
        acc = 100.0 * success / TRIAL;
        
        // 結果の表示
        std::cout << L << '\t' << acc << '\n';
        f << L << '\t' << acc << '\n';
    }

    f.close();
    return 0;
}