import os
from datetime import datetime

from PIL import Image

import image_downloader

base_dir = "./dataset/raw"  # 基础目录路径，可以根据需要修改
base_dir_clean = "./dataset/clean"  # 清洗后的图片存储目录


def create_timestamped_folder(base_dir: str, dt: datetime = None) -> str:
    """
    在指定目录下创建一个以时间命名的文件夹，格式为 'YYYYMMDD_HHMMSS'。

    参数:
        base_dir (str): 基础目录路径，例如 './images'
        dt (datetime, optional): 指定时间对象；如果不传则使用当前时间。

    返回:
        str: 创建的时间戳文件夹完整路径
    """
    if dt is None:
        dt = datetime.now()

    timestamp = dt.strftime('%Y%m%d_%H%M%S')
    folder_path = os.path.join(base_dir, timestamp)

    os.makedirs(folder_path, exist_ok=True)

    return folder_path


def convert_images_to_jpg(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for idx, file_name in enumerate(os.listdir(src_dir)):
        file_path = os.path.join(src_dir, file_name)
        if os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img:
                    rgb_img = img.convert('RGB')
                    # 截取最后一个子目录名称，也就是最后一个/和倒数第二个/中间的文本
                    last_subdir_name = os.path.basename(os.path.dirname(file_path))

                    new_file_name = f"{last_subdir_name}_{idx + 1}.jpg"
                    new_file_path = os.path.join(dst_dir, new_file_name)
                    rgb_img.save(new_file_path, 'JPEG')
                    print(f"Converted {file_name} to {new_file_name}")
            except Exception as e:
                print(f"Failed to convert {file_name}: {e}")


def crawl_from_baidu(named_entities, max_number=100, num_threads=100, timeout=20, now_time: datetime = None):
    save_folder = create_timestamped_folder(base_dir, now_time)
    clean_folder = create_timestamped_folder(base_dir_clean, now_time)
    for named_entity in named_entities:
        image_downloader.main(
            ["--engine", "Baidu", "--driver", "chrome_headless", "--max-number", str(max_number), "--num-threads", str(num_threads),
             "--timeout", str(timeout),
             "--file_prefix", "baidu_img",
             "--output",
             f"{save_folder}/{named_entity}_baidu/", named_entity]
        )
    # 清洗图片，转换格式并重命名
    for named_entity in named_entities:
        convert_images_to_jpg(f"{save_folder}/{named_entity}_baidu/", f"{clean_folder}/{named_entity}_baidu/")

def crawl_from_google(named_entities, max_number=100, num_threads=100, timeout=20, now_time: datetime = None):
    save_folder = create_timestamped_folder(base_dir, now_time)
    clean_folder = create_timestamped_folder(base_dir_clean, now_time)
    for named_entity in named_entities:
        image_downloader.main(
            ["--engine", "Google", "--driver", "chrome_headless", "--max-number", str(max_number), "--num-threads", str(num_threads),
             "--timeout", str(timeout),
             "--file_prefix", "google_img",
             "--output",
             f"{save_folder}/{named_entity}_google/", named_entity]
        )
    # 清洗图片，转换格式并重命名
    for named_entity in named_entities:
        convert_images_to_jpg(f"{save_folder}/{named_entity}_google/", f"{clean_folder}/{named_entity}_google/")

def crawl_from_bing(named_entities, max_number=100, num_threads=100, timeout=20, now_time: datetime = None):
    save_folder = create_timestamped_folder(base_dir, now_time)
    clean_folder = create_timestamped_folder(base_dir_clean, now_time)
    for named_entity in named_entities:
        image_downloader.main(
            ["--engine", "Bing", "--driver", "chrome_headless", "--max-number", str(max_number), "--num-threads", str(num_threads),
             "--timeout", str(timeout),
             "--file_prefix", "bing_img",
             "--output",
             f"{save_folder}/{named_entity}_bing/", named_entity]
        )
    # 清洗图片，转换格式并重命名
    for named_entity in named_entities:
        convert_images_to_jpg(f"{save_folder}/{named_entity}_bing/", f"{clean_folder}/{named_entity}_bing/")


if __name__ == '__main__':
    # named_entities = list(mapping_detection_annotations.keys())
    now_time = datetime.now().replace(microsecond=0)
    named_entities = ["建筑"]
    """
    Uncomment the following lines to enable crawling from different search engines.
    You can choose to crawl from Baidu, Google, or Bing.
    
    Note: Ensure that the necessary dependencies are installed and configured correctly.
    You may need to adjust the max_number, num_threads, and timeout parameters as needed.
    """

    # crawl_from_baidu(named_entities, max_number=100, num_threads=100, timeout=20, now_time=now_time)
    # crawl_from_google(named_entities, max_number=100, num_threads=100, timeout=20, now_time=now_time)
    crawl_from_bing(named_entities, max_number=10, num_threads=100, timeout=20, now_time=now_time)
