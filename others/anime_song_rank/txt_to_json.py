import json

# 读取txt文件
file_path = "others/anime_song_rank/anime_song_rank.txt"
songs = []

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(",")
        if len(parts) == 6:  
            chinese_name, japanese_name, chinese_anime_name, anime_name, score1, score2 = parts
            songs.append({
                "name": japanese_name,
                "anime": anime_name,
                "x": float(score1),
                "y": float(score2)
            })

# 写入JSON文件
with open("others/anime_song_rank/anime_song_rank.json", "w", encoding="utf-8") as json_file:
    json.dump(songs, json_file, ensure_ascii=False, indent=4)

print("✅ JSON 数据已生成：data.json")
