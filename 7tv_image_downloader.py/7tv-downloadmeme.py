from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    print(f'資料夾{folder_name}建立完成')


def download_image(url, folder_name, image_name):
    try:
        response = requests.get(url, stream = True)
        if response.status_code == 200:
            file_path = os.path.join(folder_name, image_name)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f'圖片{image_name}下載完成')
        else:
            print(f'無法下載圖片:狀態碼{response.status_code}')
    except Exception as e:
        print(f"下載圖片發生錯誤{e}")

try:
    service = Service("C:\\Users\\A7379\\OneDrive\\Desktop\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get('https://7tv.app/emotes?page=1&category=trending_day')
    count = 0
    
    #等待頁面加載
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.name'))
    )
    print('頁面加載成功!')

    folder_name = '7tv_images'
    create_folder(folder_name)

    # 印出 HTML 測試
    # page_source = driver.page_source
    # print("頁面源碼打印：")
    # print(page_source)  # 调试输出页面源码，查看表情名称元素是否正确加载

    #提取圖片
    images = driver.find_elements(By.CSS_SELECTOR, 'img.image.svelte-1d7o56f')
    # if images:
    #     print(f'找到{len(images)}張圖片')
    #     for index, img in enumerate(images, start = 1):
    #         src = img.get_attribute('src')
    #         print(f'圖片{index}:{src}')
    # else:
    #     print('未找到圖片!')
    
    #提取表情名稱
    emotes = driver.find_elements(By.CSS_SELECTOR, 'span.name.svelte-clww9e')
    # if emotes:
    #     for emote in emotes:
    #         print(emote.text)
    # else:
    #     print('沒有找到任何表情名稱！')

    for emote, img in zip(emotes, images):
        enmote_name = emote.text.strip( )
        img_url = img.get_attribute('src')

        if img_url.endswith('1x_static.png'):
            img_url = img_url.replace('1x_static.png', '3x.avif')
            
        if enmote_name and img_url and count < 10:
            download_image(img_url, folder_name, f'{enmote_name}.png')
            count += 1

    input('瀏覽器已打開,請按Enter結束...')
    
except Exception as e:
    print(f'發生錯誤: {e}')

finally:
    driver.quit()
