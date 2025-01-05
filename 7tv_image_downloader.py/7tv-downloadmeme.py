from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

def download_img(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f'圖片已儲存於 {save_path}')
        else:
            print(f'圖片下載失敗：{url}')
    except Exception as e:
        print(f'發生錯誤：{str(e)}')

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    
    driver.get('https://7tv.app/emotes?page=1&category=trending_day')
    try:
        dir_name = 'image/7tv'
        os.makedirs(dir_name, exist_ok=True)

        while True:
            print("等待圖片載入...")
            images = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.img-wrapper img'))
            )

            if not images:
                print("沒有發現圖片元素")
                break

            print(f"發現 {len(images)} 張圖片，開始下載...")
            for img in images:
                img_url = img.get_attribute('src')
                if img_url:
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    img_parts = img_url.split('/')
                    img_id = img_parts[-2]
                    img_name = f'{img_id}_{img_parts[-1]}'
                    save_path = os.path.join(dir_name, img_name)
                    download_img(img_url, save_path)

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Next page"]'))
                )
                next_button.click()
                time.sleep(2)
            except Exception:
                print('沒有下一頁了')
                break

    except Exception as e:
        print(f'發生錯誤：{e}')
    
    finally:
        driver.quit()



if __name__ == '__main__':
    main()