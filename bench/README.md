# C vs Python 速度比較（簡易）

再帰フィボナッチとエラトステネスの篩を、C と CPython で比べたもの。

## 結果

| ベンチ | C (gcc -O2) | C (gcc -O0) | Python | 比 (Python / C -O2) |
|---|---|---|---|---|
| `fib(35)` 再帰 | 0.021 s | 0.062 s | 1.03 s | 約 48 倍 |
| 篩 1000 万まで | 0.041 s | – | 1.88 s | 約 45 倍 |

## 条件

- CPU: Intel Core i5-9600（6 コア 6 スレッド）
- C: gcc 15.2.0
- Python: CPython 3.14.4（GIL あり、JIT なし）
- 計測: `date` で前後を挟んだ wall clock。プロセス起動時間込み（Python の起動は約 0.014 s）
- 回数: C の `fib(32)` と篩は 2 回、それ以外は 1 回のみ

ちゃんと比べるなら、複数回の中央値を取る、CPU 周波数を固定する、[hyperfine](https://github.com/sharkdp/hyperfine) を使う、などが必要。あくまで目安。

Rust はこのマシンにツールチェーンが無かったので測っていない。

## 再現

```sh
gcc -O2 -o fib fib.c && gcc -O2 -o sieve sieve.c
time ./fib 35
time python3 fib.py 35
time ./sieve 10000000
time python3 sieve.py 10000000
```
