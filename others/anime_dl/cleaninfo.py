import re

def clean_text(text):
    lines = text.strip().split("\n")
    lines[0] = "#" + lines[0]  # 在第一行前面加上#
    
    # 删除重复的“あとでみる” 和 “シェア”
    cleaned_lines = []
    seen = set()
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        cleaned_lines.append(line)
    
    # いいね和下一行合并
    for i, line in enumerate(cleaned_lines):
        if line == "いいね":
            cleaned_lines[i] = cleaned_lines[i] +" " + cleaned_lines[i+1]
            cleaned_lines.pop(i+1)
            break
    # 删除多余的“あとでみる” 和 “シェア”
    for i, line in enumerate(cleaned_lines):
        if line == "あとでみる":
            cleaned_lines.pop(i)
            break
    for i, line in enumerate(cleaned_lines):
        if line == "シェア":
            cleaned_lines.pop(i)
            break
    # 合并出演者部分
    出演者_index = cleaned_lines.index("出演者")
    copyright_index = next(i for i, line in enumerate(cleaned_lines) if "(C)" in line or "（C）" in line)
    出演者内容 = ", ".join(line.replace("　", "") for line in cleaned_lines[出演者_index:copyright_index])

    # 重新整理文本
    result = cleaned_lines[:出演者_index] + [出演者内容] + cleaned_lines[copyright_index:]

    return "\n".join(result)

# 示例输入
data = """
千鳥の鬼レンチャン
後半：ササキオサム ヘッドボイサー第2章
フジテレビ
2月9日(日)放送分
配信終了まで1週間以上
いいね
1,492
あとでみる
あとでみる
シェア
シェア
【次回放送は2025年2月23日（日）よる7時から　3時間SP】

今週は、数々のアニメキャラクターを演じてきた人気声優で、歌唱力の高さからミュージカル俳優としても活躍している声のエキスパート平野綾が初挑戦！前回、鬼ハードモードに挑戦するも失敗、浅岡雄也（FIELD OF VIEW）とのタッグでも敗退。今回はYouTubeでハードなボイストレーニングを重ね、進化したヘッドボイスで挑むササキオサム（MOON CHILD）！前回、持ち前の歌唱力で7レンチャンのスピリチュアル歌手・宇徳敬子が再び参戦！果たして挑戦者たちの鬼レンチャン達成となるか！？
出演者
千鳥
千鳥
かまいたち
かまいたち
平野　綾
平野　綾
佐々木　収
佐々木　収
MOON CHILD
MOON CHILD
宇徳　敬子
宇徳　敬子
（C）フジテレビ
"""

cleaned_text = clean_text(data)
print(cleaned_text)
