import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.ticker import FixedLocator
from textwrap import wrap
# 读取文件内容
file_path = 'others/anime_song_rank.txt'
songs = []

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.strip().split(',')
        if len(parts) == 6:  # 修正这里的长度检查
            chinese_name, japanese_name, chinese_anime_name, anime_name, score1, score2 = parts
            score1 = float(score1)
            score2 = float(score2)
            songs.append((chinese_name, japanese_name, chinese_anime_name, anime_name, score1, score2))

# 创建图形
fig, ax = plt.subplots()

# 设置字体
chinese_font_path = 'others/LXGWWenKai-Light.ttf'  # 这里需要指定一个支持中文的字体文件路径
japanese_font_path = 'others/LXGWWenKai-Light.ttf'  # 这里需要指定一个支持日文的字体文件路径
chinese_prop = fm.FontProperties(fname=chinese_font_path)
japanese_prop = fm.FontProperties(fname=japanese_font_path)

# 绘制点和标签
for chinese_name, japanese_name, chinese_anime_name, anime_name, score1, score2 in songs:  # 修正这里的变量解包
    ax.scatter(score1, score2)
    # ax.text(score1, score2, f' {japanese_name}\n{anime_name}', fontproperties=japanese_prop, fontsize=8, ha='right')
    wrapped_japanese_name = "\n".join(wrap(japanese_name, width=15))
    wrapped_anime_name = "\n".join(wrap(anime_name, width=10))
    ax.text(score1, score2, f' {wrapped_japanese_name}', fontproperties=japanese_prop, fontsize=11, ha='right',
            bbox=dict(boxstyle="square,pad=0.3", edgecolor='none', facecolor='none'))
    ax.text(score1, score2 - 2, f' {wrapped_anime_name}', fontproperties=japanese_prop, fontsize=6, ha='right',
            bbox=dict(boxstyle="square,pad=0.3", edgecolor='none', facecolor='none'))

# 设置标题和标签
ax.set_title('AniSong Rank', fontproperties=chinese_prop)
ax.text(-110, 0, '耐听度', ha='center', va='center', transform=ax.transData, fontproperties=chinese_prop)
ax.text(0, -110, '第一印象', ha='center', va='center', transform=ax.transData, fontproperties=chinese_prop)

# 设置坐标轴范围，使原点在 (0, 0)
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

# 设置十字架坐标系
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# 设置坐标轴的刻度
ax.set_xticks(np.arange(-100, 101, 10))
ax.set_yticks(np.arange(-100, 101, 10))
# 保持坐标轴的长宽比例相同
ax.set_aspect('equal', adjustable='box')
plt.show()