import subprocess
import logging
import os
import re

# 配置日志
logging.basicConfig(filename='D://anime//video_downloader.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取链接列表
input_file = "D://anime//list.txt"

# 下载视频
def download_video(video_url):
    try:
        # 生成安全的文件名
        safe_filename = re.sub(r'[\/:*?"<>|]', '_', video_url.split("/")[-1])  # 取URL最后一部分作为文件名
        output_path = f"D://anime//{safe_filename}.%(ext)s"

        # 下载视频
        command = ['yt-dlp', video_url, '-o', output_path, '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4']
        subprocess.run(command, check=True)
        logging.info(f"视频下载完成: {output_path}")

    except subprocess.CalledProcessError as e:
        logging.error(f"下载失败: {e}")

if __name__ == '__main__':
    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        
        for url in urls:
            logging.info(f"开始下载: {url}")
            download_video(url)
    else:
        logging.error(f"文件 {input_file} 不存在！")

# 以下内容是url网页中的元素，请每次下载视频时把这些信息找到然后写在同目录的一个同名txt文件中
# <h2 class="titles_seriesTitle__sD80N">薬屋のひとりごと</h2>
# <h1 class="titles_title__Dq6FR">第29話 月精</h1>
# <div class="description_metaDetail__pvpdu">日テレ</div>
# <div class="description_metaDetail__pvpdu">2月14日(金)23:59 終了予定<div class="description_metaDetail__pvpdu">2月7日(金)放送分</div></div>
# <div class="expandable-description_description__kS8ua">“月の精と会いたい”という特使からの無理難題に応えるため、50年以上前から花街にいた“月の精”――緑青館のやり手婆から当時の話を聞いた猫猫。特使の祖父が国に帰ってから描かせたという幻想的な絵と当時の話をもとに、猫猫は月の精が舞を披露したという後宮内の桃園へと足を運んでいた。そこへ虫を捕まえに来たという子翠と偶然出会い、話をしていると、猫猫はとある秘策を思いつく。
# そして、特使を招いた宴の日。十六夜の月が浮かぶ中、特使たちの前に美しい月の精が姿を現す―</div>
# <div class="expandable-description_copyright__8EoXW">(C)日向夏・イマジカインフォス／「薬屋のひとりごと」製作委員会</div>
