import requests
from bs4 import BeautifulSoup
import sqlite3 as db

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
}

# with db.connect('colors.db') as connect:
#     cursor = connect.cursor()
#     cursor.execute(f"""CREATE TABLE IF NOT EXISTS body_type (
#                                     body_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                     body TEXT)""")


def connection(url):
    req = requests.get(url, headers=headers)
    src = req.text
    return BeautifulSoup(src, 'lxml')

counter = 0

with db.connect('colors.db') as connect:
    cursor = connect.cursor()

    for i in range(0, 999, 1):
        link = f'https://cars.av.by/filter?page={i}'
        soup = connection(link)

        if soup.find(class_='listing__empty'):
            break

        links = soup.find_all('a', class_='listing-item__link')

        for link in links:
            final_link = 'https://cars.av.by' + link.get('href')
            new_soup = connection(final_link)

            # [2] - цвет, [0] - тип кузова
            parameter_name = new_soup.find('div', class_='card__description').text.split(',')[0].strip()
            counter += 1
            print(counter)
            cursor.execute(f"INSERT INTO body_type(body) VALUES ('{parameter_name}')")
