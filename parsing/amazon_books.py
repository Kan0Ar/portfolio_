from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import re
import pandas as pd
from time import sleep

# Список для хранения данных о книгах
books_data = []

# Куки и заголовки запроса для обхода ограничений Amazon
cookies = {
    'session-id': '144-1385442-1196540',
    'ubid-main': '130-5909207-9482235',
    'skin': 'noskin',
    'sst-main': 'Sst1|PQGdWhz42_me_aVgQIW2Vd5ZBkB13XxQhugdMnyTCodeTTLbBHOX00g-eSYcxe4LLLdp-G1N7BUsAQNcI-18AAga_RHm2NxZBnRC3aMFclx1bVzYV9HbTqyuAlCJpPKoiatBe3C8E3fyTaNCOWp6bGpTfaGa6LhIArlG1SEDN6usVP9zVfFJUADrdJaIUFiaX_RVmgpVzerifUJTMe3BZhH2GrvApjKubaS_Nu7Je717WVc',
    'JSESSIONID': 'A547738D64A822EBC7F85F560ED7BF7D',
    'session-id-time': '2082787201l',
    'i18n-prefs': 'USD',
    'appstore-devportal-locale': 'en_US',
    'at_check': 'true',
    '_mkto_trk': 'id:365-EFI-026&token:_mch-amazon.com-dce6ade633fe68e91f72375051230598',
    'AMCVS_4A8581745834114C0A495E2B%40AdobeOrg': '1',
    's_plt': '2.34',
    's_pltp': 'undefined',
    's_ips': '703',
    's_cc': 'true',
    'mbox': 'PC#3d8270609d764893b98d16955f0b11e2.37_0#1802771021|session#c5942f12d2c5419bb8fe3b6168ff27e2#1739528081',
    's_tp': '1886',
    's_ppv': 'docs%252Fmobile-associates%252Fmas-finding-product-id.html%2C37%2C37%2C703%2C1%2C2',
    'AMCV_4A8581745834114C0A495E2B%40AdobeOrg': '179643557%7CMCIDTS%7C20133%7CMCMID%7C42487999787064372631580091188933414090%7CMCAAMLH-1740131020%7C6%7CMCAAMB-1740131020%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1739533420s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-20140%7CvVersion%7C5.5.0',
    's_nr': '1739526220792-Repeat',
    's_lv': '1739526220793',
    'lc-main': 'en_US',
    'session-token': 'gUWb5Ri4VTfBPW5UdU3xtmTDrkXAWn3wqkd4gRnijrIj/jtt0GGPXBNRVAk8zAUchqLvDMreLGOdIi45fO4DTEj4eeGDniVa7vb49NvwcaWd40rkZja1m6S8/5LP6WqJSw3uXFtxbOp/vxf5ga2Nx7C5cqCfLCEHIQOxzWNS+tf+Zm4dsFgZlNbzQO0dkpDG1pEZy8+FMs8/XmEKjMAOZOFBCZblkDDjJ+FAPZKzMGBAydzGeSQfDBRs4eUVYdiEMEHyE5fynPFrKaRUMB5OxZvwHCZSaaBDpPy4csatruuNnjMHD2rdKaw6WdExDA4CjuxVqQlReDrwlqbmId9c/n1iWA+Mh2MV',
    'sp-cdn': '"L5Z9:CA"',
    'csm-hit': 'tb:XZ0GMMN1JH6WTJA1KX3R+s-PTXBHVBBQY0VX98VFM5R|1741868297315&t:1741868297315&adb:adblk_no',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-BY,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6',
    'cache-control': 'max-age=0',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1.25',
    'ect': '4g',
    'priority': 'u=0, i',
    'referer': 'https://kwork.ru/',
    'rtt': '50',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1.25',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"8.0.0"',
    'sec-ch-viewport-width': '1033',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'viewport-width': '1033',
}

# Настройка браузера
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Запуск без окна
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Запуск Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL бестселлеров Amazon
def main():
    base_url = "https://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text"
    driver.get(base_url)

    links = set()  # Используем set, чтобы сразу исключать дубликаты

    while True:
        # Прокручиваем страницу вниз, чтобы подгрузить все элементы
        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Забираем HTML после полной загрузки
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # Находим ссылки на книги
        linkedd = soup.find_all('a', class_="a-link-normal aok-block")
        for link in linkedd:
            links.add('https://www.amazon.com' + link.get('href'))

        # Ищем кнопку "Next"
        try:
            next_button = driver.find_element(By.CLASS_NAME, "a-last")
            if "a-disabled" in next_button.get_attribute("class"):
                break  # Если кнопка отключена, значит, страниц больше нет
            next_button.click()
            time.sleep(3)  # Даем странице загрузиться
        except:
            break  # Если кнопка "Next" не найдена, выходим из цикла
    driver.quit()
    
    print(f"✅ Найдено ссылок на книги: {len(links)}")
    for url in links:
        sleep(2)  # Пауза для предотвращения блокировки
        response = requests.get(url=url, cookies=cookies, headers=headers,)
        soup = BeautifulSoup(response.text, 'lxml')

        # Извлечение названия книги
        name = soup.find('span', id="productTitle", class_="a-size-large celwidget").text.strip()

        # Извлечение имени автора
        not_author = soup.find('span', class_="author notFaded")
        author = not_author.find('a', class_="a-link-normal").text.strip()

        # Формат книги (Kindle, Hardcover, Paperback и т. д.)
        book_format = soup.find('span', id="productSubtitle", class_="a-size-medium a-color-secondary celwidget").text.strip()

        # Извлечение описания книги
        desc = soup.find('div', class_="a-expander-collapsed-height a-row a-expander-container a-spacing-base a-expander-partial-collapse-container")
        try:
            try:
                description = desc.find('span', class_="a-text-italic").text.strip()
            except AttributeError:
                description = desc.find('div', class_="a-expander-content a-expander-partial-collapse-content").text.strip()
        except AttributeError:
            description = desc.find('span', class_="a-text-bold").text.strip()

        # Извлечение информации о книге
        date = soup.find('ul', class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list")
        info = date.find_all('li')
        for i in info:
            not_info = i.find('span', class_="a-list-item")
            asin = not_info.find('span', class_="a-text-bold").text.strip()
            if asin[0:12] == 'Print length':
                pages = not_info.find_all('span')[-1].text[:-6]
            else:
                pages = 'None'
            if asin[:16] == 'Publication date':
                publication_date = not_info.find_all('span')[-1].text#[:-6]
            if asin[:5] == 'X-Ray':
                x_ray = not_info.find_all('span')[-1].text
            if asin[:8] == 'Language':
                language = not_info.find_all('span')[-1].text
            if asin[:9] == 'File size':
                file_size = not_info.find_all('span')[-1].text
            if asin[:9] == 'Word Wise':
                word_wise = not_info.find_all('span')[-1].text
            if asin[:9] == 'Publisher':
                publ = not_info.find_all('span')[-1].text
                publisher = re.sub(r'\([^()]*\)', '', publ)
            if asin[:14] == 'Text-to-Speech':
                text_to_speech = not_info.find_all('span')[-1].text
            if asin[:20] == 'Enhanced typesetting':
                enhanced_typesetting = not_info.find_all('span')[-1].text
            if asin[:13] == 'Screen Reader':
                screen_reader = not_info.find_all('span')[-1].text
            else:
                continue

        # Извлечение рейтинга и отзывов
        users = soup.find('div', id="averageCustomerReviews")
        try:
            raiting = users.find('span', class_="a-size-base a-color-base").text.strip()
        except AttributeError:
            raiting = 'None'
        try:
            stars = soup.find('a', id="acrCustomerReviewLink", class_="a-link-normal").text.strip()[:-8]
        except AttributeError:
            stars = 'None'

        # Извлечение категории книги
        seller = soup.find('div', id="detailBulletsWrapper_feature_div", class_="a-section feature detail-bullets-wrapper bucket")
        sell = seller.find_all('li')
        for s in sell:
            rank = s.find('span', class_="a-list-item").text.strip()
            if rank[:17] == 'Best Sellers Rank':
                td2 = list(s.stripped_strings)
                seller_rank = re.sub(r'[^\w\s]+|[\d]+', r'', td2[1]).strip()
                category = seller_rank.lstrip('in ')

        # Извлечение цен на различные форматы книг
        all_price = soup.find('ul', id="tmmSwatchesList", class_="a-unordered-list a-nostyle a-vertical")
        try:
            not_kindle = all_price.find('div', id="tmm-grid-swatch-KINDLE", class_="a-column a-span6 a-text-left swatchElement selected celwidget", role="listitem")
            kindle_price = not_kindle.find('span', class_="slot-price").text.strip()[1:]
        except AttributeError:
            kindle_price = '0'

        try:
            not_hardcover = all_price.find('div', id="tmm-grid-swatch-HARDCOVER", class_="a-column a-span6 a-text-left swatchElement unselected celwidget", role="listitem")
            hardcover_price = not_hardcover.find('span', class_="slot-price")
            not_hard = hardcover_price.find('span').text.strip()
            if not_hard[:4] == 'from':
                hardcover_price = not_hard[6:]
            else:
                not_hardcover = all_price.find('div', id="tmm-grid-swatch-HARDCOVER", class_="a-column a-span6 a-text-left swatchElement unselected celwidget", role="listitem")
                hardcover_price = not_hardcover.find('span', class_="slot-price").text.strip()[1:]

        except AttributeError:
            hardcover_price = '0'


        try:
            not_paperback = all_price.find('div', id="tmm-grid-swatch-PAPERBACK", role="listitem")
            paperback = not_paperback.find('span', class_="slot-price").text.strip()
            if paperback.lower().startswith('from'):
                paperback_price = paperback[6:] 
            elif paperback == '—':
                paperback_price = 0 # Если цена отсутствует
            else:
                paperback_price = paperback[1:] # Убираем знак $
        except AttributeError:
            paperback_price = 0

        # Сохранение данных о книге
        books_data.append({
            "Category": category,
            "Name": name,
            "Description": description,
            "Author": author,
            "Format": book_format,
            "Amazon stars": stars,
            "Amazon rating": raiting,
            "Kindle price": kindle_price,
            "Hardcover price": hardcover_price,
            "Paperback price": paperback_price,
            "Publisher": publisher,
            "Publication date": publication_date,
            "Language": language,
            "File size": file_size,
            "Text to speech": text_to_speech,
            "Screen reader": screen_reader,
            "Enhanced typesetting": enhanced_typesetting,
            "X-Ray": x_ray,
            "Word Wise": word_wise,
            "Print length": pages,
            "URL": url
        })

        # Запись данных в Excel
        df = pd.DataFrame(books_data)
        df.to_excel("books.xlsx", index=False)
        print('Ссылка обработана и записана!')


if __name__ == '__main__':
    main()