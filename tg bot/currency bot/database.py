# модуль
import sqlite3


# бд
def main():
    connection = sqlite3.connect('myfin.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS banks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            usd_sale INTEGER,
            usd_buy INTEGER,
            eur_sale INTEGER,
            eur_buy INTEGER,
            rub_sale INTEGER,
            rub_buy INTEGER
        )
    """)
    connection.close()

if __name__ == '__main__':
    main()