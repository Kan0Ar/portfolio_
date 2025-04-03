import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

furniture_catalog = []
testr = []

cookies = {
    'aksamit_ct_ref_c': 'https://www.google.com/',
    'BITRIX_SM_GUEST_ID': '4740656',
    'PHPSESSID': 'r7LxmmiJP6HwOsdV4b7pPowsjy9D4CL1',
    'aksamit_ct_id': '17456106',
    'aksamit_ct_s': 'eyJwaG9uZXMiOnsiKzM3NTI5NjcyMzMwMCI6IiszNzU0NDc2OTQ5MzEiLCIrMzc1MjU2NzIzMzAwIjoiciIsIiszNzUzMzY3MjMzMDAiOiJyIn0sInJlZ2V4cCI6IiIsImV4cCI6IjIwMjUtMDQtMDJUMTQ6MjE6NDYuNDI2WiJ9',
    'BX_USER_ID': '95a6ea692a4d2132fb7ba1ce42d934ed',
    '_fbp': 'fb.1.1743517307170.566383476795988441',
    'aksamit_ct_fb': '1',
    'BITRIX_SM_LAST_ADV': '5',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1743541140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    'BITRIX_SM_LAST_VISIT': '01.04.2025%2017%3A22%3A06',
}
 
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://aksamit.by/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'aksamit_ct_ref_c=https://www.google.com/; BITRIX_SM_GUEST_ID=4740656; PHPSESSID=r7LxmmiJP6HwOsdV4b7pPowsjy9D4CL1; aksamit_ct_id=17456106; aksamit_ct_s=eyJwaG9uZXMiOnsiKzM3NTI5NjcyMzMwMCI6IiszNzU0NDc2OTQ5MzEiLCIrMzc1MjU2NzIzMzAwIjoiciIsIiszNzUzMzY3MjMzMDAiOiJyIn0sInJlZ2V4cCI6IiIsImV4cCI6IjIwMjUtMDQtMDJUMTQ6MjE6NDYuNDI2WiJ9; BX_USER_ID=95a6ea692a4d2132fb7ba1ce42d934ed; _fbp=fb.1.1743517307170.566383476795988441; aksamit_ct_fb=1; BITRIX_SM_LAST_ADV=5; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1743541140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; BITRIX_SM_LAST_VISIT=01.04.2025%2017%3A22%3A06',
}

def download_images(images, folder="images"):
    """Скачивает изображения и сохраняет в указанную папку."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for index, img_url in enumerate(images):
        try:
            response = requests.get(img_url, stream=True)
            response.raise_for_status()
            
            img_name = os.path.join(folder, os.path.basename(img_url))
            with open(img_name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            print(f"Скачано: {img_name}")
        except requests.RequestException as e:
            print(f"Ошибка при скачивании {img_url}: {e}")

def main():
    for value in range(1, 23):
        response = requests.get(f'https://aksamit.by/product/spalni/spalnye_garnitury/page-{value}/?ncc=1', cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        card = soup.find_all('div', class_="col-sm-4 product-item-small-card")
        for c in card:
            sleep(3)
            link = c.find('a', class_="catalog-section-item-name-link").get('href')
            
            response = requests.get(url=link, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')

            name = soup.find('h1', class_="catalog-set-element-title flex-fill g-font-size-26 g-font-weight-700 mb-3").text
            try:
                description = soup.find('div', class_="product-item-detail-tab-content", itemprop="description").text.strip()
            except AttributeError:
                description = 'None'
            ordinary_price = soup.find('strong', {"data-role": "set-old-price"}).text
            sale_price = soup.find('strong', {'data-role' : "set-price"}).text
            economy_price = soup.find('strong', {'data-role' : "set-diff-price"}).text[:-5]

            all_about_product = soup.find('div', class_="product-item-detail-tabs-container-modify flex-fill")
            if not all_about_product:
                print(f"⚠ Не найден блок характеристик на странице {link}")
                return
            

            images = []
            image_cards = soup.find_all('div', class_="product-item-detail-slider-image")
            for im in image_cards:
                img_tag = im.find('img')  # Ищем тег <img> внутри контейнера
                if img_tag:  # Проверяем, найден ли <img>
                    img_src = img_tag.get('src')
                    if img_src and not img_src.endswith('.mp4'):  # Игнорируем видеофайлы
                        image_card = 'https://aksamit.by' + img_src
                        images.append(image_card)

            print(f"Найдено {len(images)} изображений")

            rows = all_about_product.find_all('tr')

            # Создаем словарь с характеристиками и заполняем "Не указано"
            product_data = {
                "Тип": "Не указано",
                "Коллекция": "Не указано",
                "Стиль": "Не указано",
                "Цвет": "Не указано",
                "Расцветка": "Не указано",
                "Материал": "Не указано",
                "Гарантийный срок": "Не указано",
                "Срок службы": "Не указано",
                "Производитель": "Не указано",
            }

            # Заполняем словарь характеристиками
            for row in rows:
                name_cell = row.find('td', class_="cell_name")
                value_cell = row.find('td', class_="cell_value")

                if name_cell and value_cell:
                    attr_name = name_cell.text.strip()
                    attr_value = value_cell.text.strip()

                    if attr_name in product_data:
                        product_data[attr_name] = attr_value  # Обновляем словарь

            # Записываем в список
            furniture_catalog.append({
                "Название": name,
                "Описание": description,
                "Цена": ordinary_price,
                "Скидочная цена": sale_price,
                "Экономия": economy_price,
                "Тип продукта": product_data["Тип"],
                "Коллекция": product_data["Коллекция"],
                "Стиль": product_data["Стиль"],
                "Цвет": product_data["Цвет"],
                "Расцветка": product_data["Расцветка"],
                "Материал": product_data["Материал"],
                "Гарантийный срок": product_data["Гарантийный срок"],
                "Срок службы": product_data["Срок службы"],
                "Производитель": product_data["Производитель"],
                "URL": link
            })
            
            df = pd.DataFrame(furniture_catalog)
            df.to_excel("furniture_catalog.xlsx", index=False)
            print('Данные записаны в Excel!')

            download_images(images)

if __name__ == "__main__":
    main()
