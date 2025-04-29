import requests
from bs4 import BeautifulSoup

pictures = []
url = 'https://fubag.ru/catalog/benzinovye-invertornye-tsifrovye-generatory-ti/'

cookies = {
    'prefers-color-scheme': 'dark',
    'PHPSESSID': '2Ip1vBcACL27KI1IG5GGvSn3KSKT8aoV',
    'ASPRO_MAX_USE_MODIFIER': 'Y',
    'track': 'website',
    '_ym_uid': '1745936399854742710',
    '_ym_d': '1745936399',
    '_userGUID': '0:ma2lgb39:LLR1UqLew0a9WFJtKcgDuOmG6drAC2qQ',
    'dSesn': '8600328c-7f0b-5e32-f5db-34f11299feb5',
    '_dvs': '0:ma2lgb39:1z9H84cxTQhpSauzjfLUCU0ueWvt7yCm',
    '_userGUID': '0:ma2lgb39:LLR1UqLew0a9WFJtKcgDuOmG6drAC2qQ',
    '_ym_visorc': 'w',
    'r46_segment': 'A',
    'rees46_session_code': 'BkDMIiEpZu',
    'rees46_device_id': 'AleFY9poUx',
    '_ym_debug': 'null',
    'BITRIX_CONVERSION_CONTEXT_s2': '%7B%22ID%22%3A18%2C%22EXPIRE%22%3A1745960340%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    'prefers-color-scheme': 'dark',
    'BX_USER_ID': 'c8ddea431349210d0f937160c03e88f2',
    '_ym_isad': '1',
    '_gid': 'GA1.2.852778900.1745936401',
    'digi_uc': '|',
    'rees46_segment': 'A',
    'rees46_session_last_act': '1745936455432',
    '_ga_ZEG5MWK7ET': 'GS1.1.1745936401.1.1.1745936456.5.0.0',
    '_ga': 'GA1.2.727380339.1745936401',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-BY,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://fubag.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    }

response = requests.get(url=url, cookies=cookies, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

link = 'https://fubag.ru' + soup.find('a', class_="dark_link js-notice-block__title option-font-bold font_sm").get('href')
price = soup.find('span', class_="price_value").text.strip()



response = requests.get(url=link, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

name = soup.find('div', class_="topic__heading").text.strip()
description = soup.find('div', class_="content detail-text-wrap").text.strip()

articul = soup.find('span', class_="article__value", itemprop="value").text.strip()

images = soup.find_all('img', class_='lazy product-detail-gallery__picture')
for img in images:
    src = img.get('src') or img.get('data-src')  # подстраховка
    if src:
        pictures.append('https://fubag.ru' + src)

for i, url in enumerate(pictures, start=1):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'image_{i}.jpg', 'wb') as f:
            f.write(response.content)
        print(f'Скачано: image_{i}.jpg')
    else:
        print(f'Ошибка при скачивании: {url}')