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
薬屋のひとりごと
第30話 みたび、水晶宮
日テレ
2月14日(金)放送分
2月21日(金)23:59 終了予定
いいね
4,391
あとでみる
あとでみる
シェア
シェア
医官ではない猫猫が薬を作っていたことが、診療所の女官・深緑にバレてしまった。お咎めはなかったものの彼女に呼び出された猫猫は、「水晶宮の下女に薬を作ってほしい」と頼まれる。詳しく事情を聞くと、その下女は長く体調を崩し何度も診療を勧めていたにも関わらず、半月前からパタリと姿を見せなくなったという。水晶宮の侍女たちの纏う妙な空気を、梨花妃の看病の際に感じていた猫猫は不穏に思い、水晶宮を訪問する。そこには、ある秘密が隠されていて……。
出演者
悠木　碧
悠木　碧
大塚　剛央
大塚　剛央
小西　克幸
小西　克幸
種崎　敦美
種崎　敦美
石川　由依
石川　由依
木野　日菜
木野　日菜
久野　美咲
久野　美咲
瀬戸　麻沙美
瀬戸　麻沙美
島本　須美
島本　須美
(C)日向夏・イマジカインフォス／「薬屋のひとりごと」製作委員会
"""

cleaned_text = clean_text(data)
print(cleaned_text)
