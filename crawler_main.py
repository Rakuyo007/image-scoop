import os

from PIL import Image

import image_downloader


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


def crawl_from_baidu(named_entities, max_number=100, num_threads=100, timeout=20):
    for named_entity in named_entities:
        image_downloader.main(
            ["--engine", "Baidu", "--driver", "chrome_headless", "--max-number", str(max_number), "--num-threads", str(num_threads),
             "--timeout", str(timeout),
             "--file_prefix", "baidu_img",
             "--output",
             f"./dataset/raw/{named_entity}_baidu/", named_entity]
        )
    # 清洗图片，转换格式并重命名
    for named_entity in named_entities:
        convert_images_to_jpg(f"./dataset/raw/{named_entity}_baidu/", f"./dataset/clean/{named_entity}_baidu/")

def crawl_from_google(named_entities, max_number=100, num_threads=100, timeout=20):
    for named_entity in named_entities:
        image_downloader.main(
            ["--engine", "Google", "--driver", "chrome_headless", "--max-number", str(max_number), "--num-threads", str(num_threads),
             "--timeout", str(timeout),
             "--file_prefix", "google_img",
             "--output",
             f"./dataset/raw/{named_entity}_google/", named_entity]
        )
    # 清洗图片，转换格式并重命名
    for named_entity in named_entities:
        convert_images_to_jpg(f"./dataset/raw/{named_entity}_google/", f"./dataset/clean/{named_entity}_google/")

def crawl_from_bing(named_entities, max_number=100, num_threads=100, timeout=20):
    for named_entity in named_entities:
        image_downloader.main(
            ["--engine", "Bing", "--driver", "chrome_headless", "--max-number", str(max_number), "--num-threads", str(num_threads),
             "--timeout", str(timeout),
             "--file_prefix", "bing_img",
             "--output",
             f"./dataset/raw/{named_entity}_bing/", named_entity]
        )
    # 清洗图片，转换格式并重命名
    for named_entity in named_entities:
        convert_images_to_jpg(f"./dataset/raw/{named_entity}_bing/", f"./dataset/clean/{named_entity}_bing/")


if __name__ == '__main__':
    # named_entities = list(mapping_detection_annotations.keys())
    named_entities = ["建筑"]
    """
    Uncomment the following lines to enable crawling from different search engines.
    You can choose to crawl from Baidu, Google, or Bing.
    
    Note: Ensure that the necessary dependencies are installed and configured correctly.
    You may need to adjust the max_number, num_threads, and timeout parameters as needed.
    """

    # crawl_from_baidu(named_entities, max_number=100, num_threads=100, timeout=20)
    # crawl_from_google(named_entities, max_number=100, num_threads=100, timeout=20)
    crawl_from_bing(named_entities, max_number=100, num_threads=100, timeout=20)
