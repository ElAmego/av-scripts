import requests
import csv
from bs4 import BeautifulSoup
from car_list import car_list


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


# Создание csv-файла & заголовков.
def create_file(car_number_data):
    with open(f'data/{car_number_data[0]}_data.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Модель & Марка',
                'Год',
                'КПП',
                'Двигатель',
                'Кузов',
                'Пробег',
                'Цена',
                'Ссылка'
            )
        )


# Парсинг.
def parser():
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    }
    car_number_data = cars_number()
    create_file(car_number_data)
    pages = get_number()

    for i in range(1, pages+1):
        url = f'https://cars.av.by/filter?brands[0][brand]={car_number_data[1]}&page=' + str(i)

        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        cars_data = soup.find_all(class_='listing-item__wrap')
        if soup.find(class_='listing__empty'):
            break

        for car_data in cars_data:
            car_data_name = car_data.find(class_='listing-item__link').text
            car_data_year = car_data.find(class_='listing-item__params').find_all('div')[0].text
            car_data_tth = car_data.find(class_='listing-item__params').find_all('div')[1].text.split(', ')
            car_data_transmission = car_data_tth[0]
            car_data_engine = car_data_tth[1] + " " + car_data_tth[2]
            car_data_body = car_data_tth[3]
            car_data_mileage = car_data.find(class_='listing-item__params').find_all('div')[2].text
            car_data_price = car_data.find(class_='listing-item__priceusd').text
            car_data_link = 'https://cars.av.by' + car_data.find(class_='listing-item__link').get('href')

            # Запись в csv-файл.
            with open(f'data/{car_number_data[0]}_data.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerow(
                    (
                        car_data_name,
                        car_data_year,
                        car_data_transmission,
                        car_data_engine,
                        car_data_body,
                        car_data_mileage,
                        car_data_price,
                        car_data_link,
                    )
                )
        print(f'Страница {i} обработана...')

    print('Готово.')


def main():
    parser()


if __name__ == '__main__':
    main()
