# модули
import requests
from bs4 import BeautifulSoup
import sqlite3

# списки, headers
links = []
vall = []

headers  = {'User_Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}


# сбор информации банков
def settings_v():
    url = 'https://myfin.by/currency/minsk'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    ids = [14, 22, 24, 28, 56]
    for i in ids:
        data = soup.find('tr', class_='currencies-courses__row-main', id=f'bank-row-{i}')
        links.append(data)


# подключение к бд
def connection():
    connection = sqlite3.connect('myfin.db')
    cursor = connection.cursor()
    cursor.executemany('INSERT INTO banks VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)', vall)
    
    connection.commit()
    connection.close()


# обновление полученной информации от банков
def conn():
    connection = sqlite3.connect('myfin.db')
    cursor = connection.cursor()
    cursor.executemany("""UPDATE banks SET usd_sale = ?, usd_buy = ?, eur_sale = ?, eur_buy = ?, rub_sale = ?, rub_buy= ? WHERE id = 1""", ((vall[0][1], vall[0][2], vall[0][3], vall[0][4], vall[0][5], vall[0][6]),))
    cursor.executemany("""UPDATE banks SET usd_sale = ?, usd_buy = ?, eur_sale = ?, eur_buy = ?, rub_sale = ?, rub_buy= ? WHERE id = 2""", ((vall[1][1], vall[1][2], vall[1][3], vall[1][4], vall[1][5], vall[1][6]),))
    cursor.executemany("""UPDATE banks SET usd_sale = ?, usd_buy = ?, eur_sale = ?, eur_buy = ?, rub_sale = ?, rub_buy= ? WHERE id = 3""", ((vall[2][1], vall[2][2], vall[2][3], vall[2][4], vall[2][5], vall[2][6]),))
    cursor.executemany("""UPDATE banks SET usd_sale = ?, usd_buy = ?, eur_sale = ?, eur_buy = ?, rub_sale = ?, rub_buy= ? WHERE id = 4""", ((vall[3][1], vall[3][2], vall[3][3], vall[3][4], vall[3][5], vall[3][6]),))
    cursor.executemany("""UPDATE banks SET usd_sale = ?, usd_buy = ?, eur_sale = ?, eur_buy = ?, rub_sale = ?, rub_buy= ? WHERE id = 5""", ((vall[4][1], vall[4][2], vall[4][3], vall[4][4], vall[4][5], vall[4][6]),))

    connection.commit()
    connection.close()



# добавление информации
def get_n_v():
    settings_v()
    for l in links:
        name = l.find('span').text.strip()
        vals = l.find('td', class_="pos-r").find_next_siblings("td")
        vall.append([name, vals[0].text, vals[1].text, vals[2].text, vals[3].text, vals[4].text, vals[5].text])


# обновление бд
def updating_db():
    get_n_v()
    conn()

# создание бд
def make_db():
    get_n_v()
    connection()