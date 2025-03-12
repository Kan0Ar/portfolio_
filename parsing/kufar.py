# модули

from bs4 import BeautifulSoup
import requests
from time import sleep
import sqlite3

information = []

# база данных
def sqlition():
    connection = sqlite3.connect('kufar.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS apartment(
            id INTEGER,
            description TEXT,
            price TEXT,
            rooms INTEGER,
            floor INTEGER,
            adress TEXT PRIMARY KEY,
            living area TEXT,
            total area TEXT,
            link TEXT
        )
    """)
    connection.close()


def not_main():
    # url, headers
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}
    url = 'https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno'

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # сбор ссылок
    links = soup.find('div', class_="styles_links__inner__g3xjS").get('href')
    # разбор ссылок на карточки
    for l in links:
        response = requests.get(url=l, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        cards = soup.find('div', class_="styles_wrapper__vfncA")
        card = cards.find_all('section')
        for c in card:
            sleep(1) # остановка
            links = c.find('a', class_="styles_wrapper__Q06m9").get('href')
            response = requests.get(url=links, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            all_info = soup.find_all('div', class_="styles_parameter_value__BkYDy")
            try:
                # сбор информации
                price = soup.find('span', class_="styles_main__eFbJH").text
                rooms = all_info[0].text
                total_area = all_info[1].text
                living_area = all_info[2].text
                floor = all_info[12].text
                address = soup.find('span', class_="styles_text__TdO_w").text
                description = soup.find('h1', class_="styles_adview_title__i1NEe").text
                information.append((description, price, rooms, floor, address, living_area, total_area, links))
                print('Страница обработана')
            except AttributeError:
                information.append(('None'))


# подключение к бд + сохранение информации
def main():
    not_main()
    connection = sqlite3.connect('kufar.db')
    cursor = connection.cursor()
    cursor.executemany('INSERT INTO apartment VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)', information)
    
    connection.commit()
    connection.close()


# запуск
if __name__ == '__main__':
    main()