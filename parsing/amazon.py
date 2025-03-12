# импорт модулей
import requests
from bs4 import BeautifulSoup
import sqlite3
from time import sleep

# headers, cookies и тд(curl)

items = []

params = {
    'k': 'gaming hats',
    '_encoding': 'UTF8',
    'content-id': 'amzn1.sym.09483392-9ac6-434a-a3d7-39d83662f54a',
    'pd_rd_r': '87035633-56f9-4120-8390-e0c58a8f1dc4',
    'pd_rd_w': 'UALxS',
    'pd_rd_wg': 'Gf3dK',
    'qid': '1739343174',
    'xpid': 'mNrmTK10XfHyd',
    'ref': 'sr_pg_1',
}

cookies = {
    'session-id': '144-1385442-1196540',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'sp-cdn': '"L5Z9:BY"',
    'ubid-main': '130-5909207-9482235',
    'session-token': 'z6fF4IU3QVnRHOgOsxi/6IGOCyeDECBe29hmX65twCmY6hLVdDF3YYzV/OXrus9y5k2A1AN55JsQF88A+KfwzTRsLYicSqKLIV8f1PsXsDPTF+9RPKkYe7yIIID2cM5BHtlYI8bd9x16PJu008zI6dyWqQdyrEooKVamlt27Sbt8nbJ/ir2iumvOvshmFXj949zWWPs4Sr0MooU+2OTlTeWTDnAU5wzJ/20wKRzXHaLqbwOCrkOl37xbhTW629iL3cTXamZOz/MnMj4TJ/xp4CEO0YmkcsaMlmHR9/2SZrqTvhMx+NSdhqv9crjODvvrm/D1jH52zUeBsqD6ZIbyX9UzeQ1tDGAW',
    'csm-hit': 'tb:A2J761BQ5G80SG6Z318A+sa-N51ESFHNS5ZX397RZBYW-VFZPFSM7KT4T3Q3GPME7|1739343525636&t:1739343525636&adb:adblk_no',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-BY,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6',
    'cache-control': 'no-cache',
    # 'cookie': 'session-id=144-1385442-1196540; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:BY"; ubid-main=130-5909207-9482235; session-token=z6fF4IU3QVnRHOgOsxi/6IGOCyeDECBe29hmX65twCmY6hLVdDF3YYzV/OXrus9y5k2A1AN55JsQF88A+KfwzTRsLYicSqKLIV8f1PsXsDPTF+9RPKkYe7yIIID2cM5BHtlYI8bd9x16PJu008zI6dyWqQdyrEooKVamlt27Sbt8nbJ/ir2iumvOvshmFXj949zWWPs4Sr0MooU+2OTlTeWTDnAU5wzJ/20wKRzXHaLqbwOCrkOl37xbhTW629iL3cTXamZOz/MnMj4TJ/xp4CEO0YmkcsaMlmHR9/2SZrqTvhMx+NSdhqv9crjODvvrm/D1jH52zUeBsqD6ZIbyX9UzeQ1tDGAW; csm-hit=tb:A2J761BQ5G80SG6Z318A+sa-N51ESFHNS5ZX397RZBYW-VFZPFSM7KT4T3Q3GPME7|1739343525636&t:1739343525636&adb:adblk_no',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1.25',
    'ect': '4g',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.amazon.com/ref=nav_logo',
    'rtt': '50',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1.25',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"8.0.0"',
    'sec-ch-viewport-width': '871',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'viewport-width': '871',
}

def not_main():
    # парсинг всех страниц
    for value in range(1, 8):
        url = f'https://www.amazon.com/s?k=gaming+hats&page={value}&_encoding=UTF8&content-id=amzn1.sym.09483392-9ac6-434a-a3d7-39d83662f54a&dib=eyJ2IjoiMSJ9.XAVI1LfPyXm7gKIfg0vGsSnLdd150_C-evnHFTTx2DGpwcdeU8y_7SwJXVnuBuUs7C2GH7V0F9KBlSKVQvM_ZtTy7AUDlsaIpWp3NmzbFQ02xCLRhPAcWX1wSmrBTYrgesEx24y6DHPCPf2kLifGO-jEwvnDCqlO5rtbjfYAModpswje2DChGTMbaNiyJnketm-JfIgTI1Y2uSZ6GRb20eUNRyYXbTJpchfRtp6pDkKpoTRDkkcGbLPqXFwMrvglcAxHhaZauVzoh5lCp9r73lsf5P8BA2HcuAdKpqltbo8.x2zyJJRJKA5ytobXzFd8M9pH4bJWucDimp7VfHba02E&dib_tag=se&pd_rd_r=87035633-56f9-4120-8390-e0c58a8f1dc4&pd_rd_w=UALxS&pd_rd_wg=Gf3dK&qid=1741179835&refresh=1&sr=8-1&xpid=mNrmTK10XfHyd&ref=sr_pg_2'
        response = requests.get(url=url, headers=headers, params=params, cookies=cookies)
        links = []
        soup = BeautifulSoup(response.text, 'lxml')
        # сбор ссылок карточек
        data = soup.find('div', class_="s-main-slot s-result-list s-search-results sg-row")
        card = data.find_all('div', role="listitem")
        for c in card:
            try:
                link = 'https://www.amazon.com' + c.find('a', class_="a-link-normal s-line-clamp-4 s-link-style a-text-normal").get('href')
                # сохранение ссылок в список
                links.append(link)
            except AttributeError:
                continue

        # парсинг информации с карточек
        for l in links:
            sleep(2) # перерывы
            response = requests.get(url=l, headers=headers, params=params, cookies=cookies)
            soup = BeautifulSoup(response.text, 'lxml')

            print(f'Обработка ссылки {l}\n\n')

            # сбор названий товаров
            try:
                name = soup.find('span', id="productTitle").text.strip()
            except AttributeError:
                name = 'None'


            # сбор цен товаров
            try:
                try:
                    price = soup.find('span', class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay").text.strip()
                except AttributeError:
                    not_price = soup.find('table', class_="a-lineitem a-align-top")
                    pre_price = not_price.find_all('span', class_="a-offscreen")#.text.strip()# + not_price.find
                    price = f'{pre_price[0].text} / {pre_price[-1].text}'
            except AttributeError:
                price = 'None'


            # сбор рейтинга товаров
            try:
                pre_raiting = soup.find('span', id="acrPopover", class_="reviewCountTextLinkedHistogram noUnderline")
                raiting = pre_raiting.find('span', class_="a-size-base a-color-base").text.strip()
            except AttributeError:
                raiting = 'None'


            # сбор кол-ва отзывов
            try:
                assessments = soup.find('span', id="acrCustomerReviewText").text
            except AttributeError:
                assessments = 'None'


            # сбор информации о товаре
            try:
                try:
                    about_item = soup.find('div', id="feature-bullets", class_="a-section a-spacing-medium a-spacing-top-small").text.strip()
                except AttributeError:
                    about_item = soup.find('ul', class_="a-unordered-list a-vertical a-spacing-small").text.strip()
            except AttributeError:
                about_item = 'None'


            # сбор артикулов(ASIN) товара
            try:
                data = soup.find('table', id="productDetails_detailBullets_sections1")
                articul_pref = data.find_all('tr')[-5]
                not_articul = articul_pref.find('td', class_="a-size-base prodDetAttrValue").text.strip()
            except AttributeError:
                data = soup.find('ul', class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
                artick = data.find_all('li')
                for art in artick:
                    not_articul = art.find('span', class_="a-list-item")
                    asin = not_articul.find('span', class_="a-text-bold").text.strip()
                    pre_articul = asin[0:4]
                    if pre_articul == 'ASIN':
                        articul = not_articul.find_all('span')[-1].text
                    else:
                        continue

            
            # сохранение всей информации в список
            items.append((name, price, raiting, assessments, about_item, articul, l))


# база данных 
def sqlition():
    connection = sqlite3.connect('amazon.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product(
            name TEXT,
            cost TEXT,
            raiting INTEGER,
            assessments INTEGER,
            about TEXT,
            articul TEXT PRIMARY KEY,
            link TEXT
        )
    """)
    connection.close()


# сохранение информации в базу данных
def main():
    sqlition()
    not_main()
    connection = sqlite3.connect('amazon.db')
    cursor = connection.cursor()
    try:
        cursor.executemany('INSERT OR IGNORE INTO product VALUES (?, ?, ?, ?, ?, ?, ?)', items)
    except sqlite3.DatabaseError:
        cursor.executemany('REPLACE INTO product VALUES (?, ?, ?, ?, ?, ?, ?)', items)        
    connection.commit()
    connection.close()



# запуск
if __name__ == '__main__':
    main()