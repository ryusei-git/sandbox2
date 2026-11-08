"""ぺこーらおみくじ。引数に名前を渡すと、その名前と今日の日付で結果が決まる（同じ日は何回引いても同じ）。

    python3 omikuji.py           # ランダム
    python3 omikuji.py ryupo     # ryupo の今日の運勢
"""
import datetime
import hashlib
import random
import sys

FORTUNES = [
    ("大吉", "今日は何やってもうまくいくぺこ。コンパイルも一発で通るぺこ"),
    ("中吉", "そこそこいい日ぺこ。テストは全部緑ぺこ。たぶん"),
    ("小吉", "ちょっといいことあるぺこ。牛丼に肉が多めに入ってるとかぺこ"),
    ("吉", "普通ぺこ。普通が一番ぺこ"),
    ("末吉", "後半から運が来るぺこ。夜に本気出すぺこ"),
    ("凶", "pushする前にもう一回 git diff 見るぺこ"),
    ("大凶", "今日は本番にデプロイしちゃだめな日ぺこ。ルートキー直書き厳禁ぺこ"),
]

LUCKY = ["Rust", "角煮", "UNIXパイプ", "キャッシュヒット", "hyperfine", "白髪ねぎ", "gain-shape VQ", "セグフォしないC"]


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else None
    if name:
        seed = f"{name}-{datetime.date.today().isoformat()}"
        rng = random.Random(int(hashlib.sha256(seed.encode()).hexdigest(), 16))
    else:
        rng = random.Random()
    rank, message = rng.choice(FORTUNES)
    who = f"{name}の" if name else ""
    print(f"{who}今日の運勢：【{rank}】")
    print(message)
    print(f"ラッキーアイテム：{rng.choice(LUCKY)}")


if __name__ == "__main__":
    main()
