import requests
from bs4 import BeautifulSoup
import os
import time

base_url = "http://www.glass.umd.edu/NPP/MODIS/500m/GLASS_NPP_500M_V60/"
output_path = r"G:\DATA\植被\LAI（叶面积指数）\LAI逐月数据2000-2020"

# 设定最大重试次数
max_retries = 5

# 设置延迟时间
delay_time = 3  # 3秒的延迟

for year_sequence in range(2000, 2021):
    yearly_file_download_urls = []
    for day in range(1, 362, 8):
        file_folder = f"{year_sequence}/{day:03}"
        base_file_url = f"{base_url}{file_folder}/"

        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(base_file_url, timeout=120)
                print(f"The code is {response.status_code}!")
                if response.status_code == 200:
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    links = soup.find_all('a')

                    for link in links:
                        hdf_link = link.get('href')
                        if hdf_link.endswith('.hdf'):
                            file_url = f"{base_file_url}{hdf_link}"
                            print(file_url)
                            yearly_file_download_urls.append(file_url)
                    break  # 成功获取链接，跳出重试循环
                else:
                    retries += 1  # 如果响应码非200，增加重试次数
                    time.sleep(delay_time)  # 在每次请求之后加入延迟
            except requests.Timeout:
                retries += 1  # 如果超时，增加重试次数
                time.sleep(delay_time)  # 在每次请求之后加入延迟

    for yearly_file_download_url in yearly_file_download_urls:
        file_name = yearly_file_download_url.split('/')[-1]
        output_file_name = os.path.join(output_path, f'LAI{year_sequence}_8_time_res', file_name)

        if os.path.exists(output_file_name):
            print(f'The file {output_file_name} is existed.')
            continue
        else:
            os.makedirs(os.path.dirname(output_file_name), exist_ok=True)

        retries = 0
        while retries < max_retries:
            try:
                down_response = requests.get(yearly_file_download_url, timeout=120)
                print(f'The code is {down_response}.')
                if down_response.status_code == 200:
                    with open(output_file_name, 'wb') as f:
                        f.write(down_response.content)
                        print(f"Downloaded {file_name}")
                    break  # 成功下载文件，跳出重试循环
                else:
                    retries += 1  # 如果响应码非200，增加重试次数
                    time.sleep(delay_time)  # 休眠5秒后再次尝试
            except requests.Timeout:
                retries += 1  # 如果超时，增加重试次数
                time.sleep(delay_time)  # 休眠5秒后再次尝试

print('done!')
