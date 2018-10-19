import copy
import random
from tqdm import trange

N = 100  # 入力信号の要素数
L_max = int(0.4 * N)
TRIAL = 1000  # 試行回数
REPEAT = 10  # 想起を繰り返す回数
PROT = False
GPU = False

if GPU:
    PROT = False
    from gpu import np
    print('GPU mode')
else:
    import numpy as np
    print('CPU mode')

def plus_or_not():
    """-1か+1をランダムに返す"""
    return random.choice([1, -1])

def make_memory_patterns(L):
    """記憶パターン(N×L行列)を生成する"""
    e = np.zeros((L, N), dtype=np.int8)
    for i in range(L):
        for j in range(N):
            e[i][j] = plus_or_not()
    return e

def make_coupling_matrix(e, L):
    """記憶パターンから結合係数行列を作成する"""
    w = np.zeros((N, N), dtype=np.float16)
    for i in range(N):
        for j in range(N):
            w[i][j] = sum(e[r][i] * e[r][j] for r in range(L)) / N
            if i == j: w[i][j] = 0.0
    return w

def make_input_pattern():
    """入力信号(1×N行列)を生成する"""
    return np.array([plus_or_not() for i in range(N)], dtype=np.int8)

def signal(x):
    """入力値が正なら+1, 負なら-1, 0なら0を返す"""
    return 1 if x > 0 else (-1 if x < 0 else 0)

def remember(x, w):
    """入力信号xから出力信号yを想起する"""
    return np.dot(w, x)

def eval_m(y, ans):
    """出力ベクトルと記憶ベクトルとの一致率を計算する"""
    return sum(ans[i] * y[i] for i in range(N)) / N

def run(L):
    """記憶パターン数:Lのときの想起成功率"""
    e = make_memory_patterns(L)
    w = make_coupling_matrix(e, L)
    success = 0

    for _ in trange(TRIAL, desc='Trial'):
        r = np.random.randint(L)
        ans = copy.deepcopy(e[r])  # 正解ベクトル
        x = copy.deepcopy(ans)
        noise_pos = np.random.randint(N)  # ノイズを加える位置をランダムに決定
        x[noise_pos] = -ans[noise_pos]  # 符号反転

        for _ in range(REPEAT):
            y = remember(x, w)
            if list(x) == list(y): break
            x = copy.deepcopy(y)
        m = eval_m(y, ans)

        if m == 1.0: success += 1
    acc = success / TRIAL * 100
    return acc

def main():
    with open('log.txt', 'w') as f:
        f.write('')
    L_list = [L + 1 for L in range(L_max)]
    accs = []
    for L in trange(L_max, desc='L    '):
        acc = run(L + 1)
        accs.append(acc)
        with open('log.txt', 'a') as f:
            f.write('{}\t{:.2f}\n'.format(L+1, acc))

    print()
    for L, acc in zip(L_list, accs):
        print('L: {}\tacc. {:.2f}'.format(L, acc))

    # plot
    if PROT:
        import matplotlib.pyplot as plt
        plt.plot(L_list, accs)
        plt.xlabel('L')
        plt.ylabel('平均成功率[%]')
        plt.ylim(0.0, 110.0)
        plt.show()


if __name__ == '__main__':
    main()
