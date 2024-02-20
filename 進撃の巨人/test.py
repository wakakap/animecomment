import os
from PIL import Image

def compress_image(input_path, output_path, target_size_kb=700):
    """
    压缩图片直到大小小于目标大小，并保存到输出路径
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param target_size_kb: 目标图片大小（KB）
    """
    img = Image.open(input_path)
    quality = 85
    while os.path.getsize(output_path) > target_size_kb * 1024:
        img.save(output_path, quality=quality)
        quality -= 5
        if quality <= 5:
            break

def compress_images_in_directory(input_dir, output_dir, target_size_kb=700):
    """
    在指定目录中压缩所有图片文件
    :param input_dir: 输入目录
    :param output_dir: 输出目录
    :param target_size_kb: 目标图片大小（KB）
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # 检查是否为图片文件（PNG或JPEG格式）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Compressing {input_path}...")
            compress_image(input_path, output_path, target_size_kb)
        else:
            print(f"Ignoring {input_path} (not a PNG or JPEG)")

if __name__ == "__main__":
    input_directory = input("请输入要压缩图片的目录路径: ")
    output_directory = input("请输入压缩后图片保存的目录路径: ")
    target_size_kb = int(input("请输入目标图片大小（KB，默认为700）: ") or 700)

    compress_images_in_directory(input_directory, output_directory, target_size_kb)
    print("压缩完成！")
