import requests
from bs4 import BeautifulSoup
from car_list import car_list
import sqlite3 as db
import unicodedata


# Получение цифры для ссылки по марке авто.
def cars_number():
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


# Получение и проверка на цифру/число.
def get_number():
    while True:
        try:
            number = int(input('Введите число: '))
        except ValueError:
            print('Введите корректное число.')
        else:
            break
    return number


# Парсинг.
def parser(car_number_data, pages):
    car_db = []

    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    }

    for i in range(1, pages+1):
        url = f'https://cars.av.by/filter?brands[0][brand]={car_number_data[1]}&page=' + str(i)

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


def write_in_db(cars_db, car_marka):
    with db.connect('cars.db') as connect:
        cursor = connect.cursor()
        create_table(cursor, car_marka)

        for car in cars_db:
            cursor.execute(f"""INSERT INTO {car_marka[0]} (name, year, transmission, engine, body, mileage, price, link)
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


def create_table(cursor, car_marka):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {car_marka[0]} (
                                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                year TEXT,
                                transmission TEXT,
                                engine TEXT,
                                body TEXT,
                                mileage TEXT,
                                price TEXT,
                                link TEXT)""")


def main():
    car_number = cars_number()
    pages = get_number()
    cars = parser(car_number, pages)
    write_in_db(cars, car_number)


if __name__ == '__main__':
    main()
