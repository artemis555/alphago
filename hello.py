import os
import cv2
import numpy as np
import sys

def create_images_from_binary(input_file, image_folder):
    # 读取二进制文件
    with open(input_file, 'rb') as f:
        data = f.read()

    # 创建图片文件夹
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for i, byte in enumerate(data):
        # 创建一个黑色图像
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        # 将字节值写入图像
        img[:] = byte
        # 保存图像
        cv2.imwrite(os.path.join(image_folder, f'frame_{i:04d}.png'), img)

def create_video_from_images(image_folder, output_file, duration):
    # 获取图片列表
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # 确保顺序

    # 使用ffmpeg生成视频
    os.system(f'ffmpeg -framerate {len(images) / (duration / 1000)} -i {image_folder}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p {output_file}')

def main():
    if len(sys.argv) != 4:
        print("Usage: python encode.py <input_file> <output_file> <duration_ms>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    duration = int(sys.argv[3])

    image_folder = 'images'
    create_images_from_binary(input_file, image_folder)
    create_video_from_images(image_folder, output_file, duration)

if __name__ == '__main__':
    main()

