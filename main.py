import requests
from bs4 import BeautifulSoup
from car_list import car_list
import sqlite3 as db
import unicodedata


# Получение марки авто.
def car_name():
    cars = car_list()
    while True:
        name = input('Введите марку авто. Пример: bmw, alfa_romeo.:')
        if name in cars:
            return [
                name,
                str(cars.get(name)),
            ]
        else:
            print('Название авто введено некорректно или такого нету.')


# Получение кол-ва страниц.
def get_pages():
    while True:
        try:
            pages = int(input('Введите кол-во страниц: '))
        except ValueError:
            print('Введите корректное кол-во.')
        else:
            break
    return pages


# Парсинг.
def parser(name_info, pages):
    car_db = []

    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    }

    for i in range(1, pages+1):
        url = f'https://cars.av.by/filter?brands[0][brand]={name_info[1]}&page=' + str(i)

        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml',)

        cars_data = soup.find_all(class_='listing-item__wrap')
        if soup.find(class_='listing__empty'):
            break

        for car_data in cars_data:
            car_data_tth = car_data.find(class_='listing-item__params').find_all('div')[1].text.split(', ')

            car = {
                'name': unicodedata.normalize('NFKD', car_data.find(class_='listing-item__link').text),
                'year': unicodedata.normalize('NFKD', car_data.find(class_='listing-item__params')
                                              .find_all('div')[0].text),
                'transmission': unicodedata.normalize('NFKD', car_data_tth[0]),
                'engine': unicodedata.normalize('NFKD', car_data_tth[1] + " " + car_data_tth[2]),
                'body': unicodedata.normalize('NFKD', car_data_tth[3]),
                'mileage': unicodedata.normalize('NFKD', car_data.find(class_='listing-item__params')
                                                 .find_all('div')[2].text),
                'price': unicodedata.normalize('NFKD', car_data.find(class_='listing-item__priceusd').text),
                'link': unicodedata.normalize('NFKD', 'https://cars.av.by' + car_data
                                              .find(class_='listing-item__link').get('href')),
            }

            car_db.append(car)

        print(f'Страница {i} обработана...')

    print('Готово.')
    return car_db


# Создание таблицы в БД.
def create_table(cursor, name):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name[0]} (
                                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                year TEXT,
                                transmission TEXT,
                                engine TEXT,
                                body TEXT,
                                mileage TEXT,
                                price TEXT,
                                link TEXT)""")


# Запись данных в БД.
def write_in_db(cars, name):
    with db.connect('cars.db') as connect:
        cursor = connect.cursor()
        create_table(cursor, name)
        links_in_db = get_links(cursor, name[0])

        for car in cars:
            if car['link'] not in links_in_db:
                cursor.execute(f"""INSERT INTO {name[0]} (name, year, transmission, engine, body, mileage, price, link)
                VALUES (
                '{car['name']}',
                '{car['year']}',
                '{car['transmission']}',
                '{car['engine']}',
                '{car['body']}',
                '{car['mileage']}',
                '{car['price']}',
                '{car['link']}'
                )""")


# Получение ссылок из таблицы.
def get_links(cursor, name):
    links_arr = []
    cursor.execute(f"SELECT link FROM {name}")
    for link in cursor.fetchall():
        links_arr.append(' '.join(link))
    return links_arr


def main():
    name = car_name()
    pages = get_pages()
    cars = parser(name, pages)
    write_in_db(cars, name)


if __name__ == '__main__':
    main()
