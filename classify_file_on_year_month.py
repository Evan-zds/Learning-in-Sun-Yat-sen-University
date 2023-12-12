import os
import shutil
import re

# 源文件夹路径
path = r'I:\DATA\全球PML_V2陆地蒸散发与GPP（2002.07-2019.08）'
for sub_folder in os.listdir(path):
    sub_path = os.path.join(path, sub_folder)
    if os.path.isfile(sub_path):
        continue
    else:
        source_folder = sub_path
        # 目标文件夹路径
        destination_folder = sub_path

        # 获取源文件夹中的文件列表
        files = os.listdir(source_folder)

        # 正则表达式来匹配文件名中的年份信息（假设年份格式为"YYYY"）
        year_pattern = re.compile(r'\d{4}')

        for filename in files:
            # 在文件名中查找年份信息
            match = year_pattern.search(filename)
            if match:
                # 获取匹配到的年份信息
                year_str = match.group(0)

                # 创建目标文件夹路径
                year_folder = os.path.join(destination_folder, year_str)
                os.makedirs(year_folder, exist_ok=True)  # 如果文件夹不存在，则创建

                # 构建源文件路径和目标文件路径
                source_file_path = os.path.join(source_folder, filename)
                destination_file_path = os.path.join(year_folder, filename)

                # 移动文件到目标文件夹
                shutil.move(source_file_path, destination_file_path)
                print(f"Moved {filename} to {year_folder}")
