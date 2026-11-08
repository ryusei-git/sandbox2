# メッセージ処理の流れ

Discord のメッセージがぺこーら（Claude Code + Discord プラグイン）に届いて、返信が投稿されるまで。

![message flow](message_flow.png)

`message_flow.py` で生成（Pillow と Noto Sans CJK が必要）。

```sh
python3 message_flow.py
```
