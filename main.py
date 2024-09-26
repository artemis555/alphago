import os
import cv2
import numpy as np
import sys

def extract_images_from_video(video_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 使用ffmpeg提取帧
    os.system(f'ffmpeg -i {video_file} {output_folder}/frame_%04d.png')

def decode_images_to_binary(image_folder, output_file, validity_file):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # 确保顺序

    binary_data = bytearray()
    validity_data = bytearray()

    for img_name in images:
        img_path = os.path.join(image_folder, img_name)
        img = cv2.imread(img_path)

        # 假设图像是100x100的黑色图像，提取字节值
        byte_value = img[0, 0, 0]  # 获取第一个像素的值
        binary_data.append(byte_value)

        # 假设有效性检查
        validity_data.append(1)  # 这里可以添加实际的有效性检查逻辑

    with open(output_file, 'wb') as f:
        f.write(binary_data)

    with open(validity_file, 'wb') as f:
        f.write(validity_data)

def main():
    if len(sys.argv) != 4:
        print("Usage: python decode.py <video_file> <output_file> <validity_file>")
        return

    video_file = sys.argv[1]
    output_file = sys.argv[2]
    validity_file = sys.argv[3]

    image_folder = 'extracted_images'
    extract_images_from_video(video_file, image_folder)
    decode_images_to_binary(image_folder, output_file, validity_file)

if __name__ == '__main__':
    main()
