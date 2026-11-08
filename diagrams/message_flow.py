from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
import os
if not os.path.exists(BOLD):
    BOLD = FONT
f_title = ImageFont.truetype(BOLD, 34, index=0)
f_head = ImageFont.truetype(BOLD, 25, index=0)
f_body = ImageFont.truetype(FONT, 21, index=0)
f_mono = ImageFont.truetype(FONT, 19, index=0)

W = 1000
PAD = 40
BOXW = W - 2 * PAD

# (where, color, heading, [lines], mono?)
steps = [
    ("Discord", "#5865F2", "① ユーザーがメンションして送信",
     ["「@ぺこーら あーそーぼ」"], False),
    ("ryupoのPC", "#2E7D32", "② Discordプラグイン（MCPサーバー）が受信",
     ["・botとしてDiscordにログインして、メッセージを常に受け取ってる",
      "・送信者IDとチャンネルが許可リストにあるか確認",
      "・ぺこーらへのメンションがあるか確認 → なければ無視"], False),
    ("ryupoのPC", "#2E7D32", "③ Claude Codeの会話に「外部メッセージ」として差し込む",
     ['<channel source="discord" chat_id="8317…"',
      '  user="someone" ts="2026-11-08T07:46Z">',
      '  @ぺこーら あーそーぼ',
      '</channel>'], True),
    ("ryupoのPC", "#2E7D32", "④ Claude Codeがプロンプトを組み立てる（約8万トークン）",
     ["[システムプロンプト・ツール定義・メモ]  ← 毎回同じ部分",
      "[これまでの会話（古い分は要約済み）]",
      "[③の新しいメッセージ]                       ← 今回の追加分",
      "※前回と同じ先頭部分はキャッシュされてて、毎回全部計算し直さない"], False),
    ("Anthropic", "#C2410C", "⑤ Anthropic API（Claude Opus 5.5）",
     ["・テキストをトークン（数字の列）に変換",
      "・モデルが次のトークンを1個ずつ予測して文章を作る",
      "・出力は「普通の文」か「ツール呼び出し」",
      '  例：reply(chat_id="8317…", text="いいぺこ。何するぺこ？…")'], False),
    ("ryupoのPC", "#2E7D32", "⑥ Claude Codeがツール呼び出しを実行",
     ["・reply → Discordプラグインに「この文を投稿して」と渡す",
      "・ツールを使わない普通の文は、ryupoのターミナルにだけ表示"], False),
    ("Discord", "#5865F2", "⑦ プラグインがDiscordのAPIで投稿 → チャンネルに表示",
     ["ぺこーら「いいぺこ。何するぺこ？…」"], False),
]

def box_height(lines, mono):
    lh = 28 if mono else 31
    return 16 + 36 + lh * len(lines) + 18

H = 120 + sum(box_height(l, m) + 56 for _, _, _, l, m in steps) + 20
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
d.text((PAD, 30), "Discordのメッセージがぺこーらに届いて返るまで", font=f_title, fill="#111")

y = 110
for i, (where, color, head, lines, mono) in enumerate(steps):
    h = box_height(lines, mono)
    d.rounded_rectangle([PAD, y, PAD + BOXW, y + h], radius=14, outline=color, width=3, fill="#FAFAFA")
    # location tag
    tw = d.textlength(where, font=f_body)
    d.rounded_rectangle([PAD + BOXW - tw - 30, y + 12, PAD + BOXW - 12, y + 44], radius=8, fill=color)
    d.text((PAD + BOXW - tw - 21, y + 13), where, font=f_body, fill="white")
    d.text((PAD + 20, y + 12), head, font=f_head, fill="#111")
    ty = y + 16 + 36
    for ln in lines:
        if mono:
            d.rectangle([PAD + 20, ty - 2, PAD + BOXW - 20, ty + 26], fill="#EEF2F7")
            d.text((PAD + 30, ty), ln, font=f_mono, fill="#1F3A5F")
            ty += 28
        else:
            d.text((PAD + 24, ty), ln, font=f_body, fill="#333")
            ty += 31
    y += h
    if i < len(steps) - 1:
        cx = W // 2
        d.line([cx, y + 6, cx, y + 44], fill="#888", width=4)
        d.polygon([(cx - 12, y + 38), (cx + 12, y + 38), (cx, y + 52)], fill="#888")
    y += 56

img = img.crop((0, 0, W, y))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "message_flow.png")
img.save(out)
print(out, img.size)
