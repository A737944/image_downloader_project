import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_img(url, save_path):
    try:
        print(f'正在下載圖片: {url}')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f'圖片已儲存於 {save_path}')
        else:
            print(f"下載失敗 HTTP 狀態碼: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"下載圖片時發生錯誤: {e}")
    print("-" * 30)

def main():
    url = 'https://www.ptt.cc/bbs/C_Chat/M.1726802950.A.29D.html'
    headers = {
        'Cookie': 'over18=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果請求失敗，會拋出錯誤
    except requests.exceptions.RequestException as e:
        print(f"請求失敗: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    spans = soup.find_all('span', class_="article-meta-value")
    if len(spans) < 3:
        print("標題無法找到，請確認網頁結構是否變更。")
        return

    title = spans[2].text.strip()

    # 建立資料夾
    dir_name = f'images/{title}'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    links = soup.find_all('a')
    allowed_file_types = ['jpg', 'png', 'jpeg', 'gif']

    for link in links:
        href = link.get('href')
        if not href:
            continue

        file_name = href.split("/")[-1]
        extension = href.split('.')[-1].lower()

        if extension in allowed_file_types:
            full_url = urljoin(url, href)  # 處理相對路徑
            save_path = os.path.join(dir_name, file_name)
            download_img(full_url, save_path)

if __name__ == "__main__":
    main()
