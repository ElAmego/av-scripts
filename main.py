import requests
from bs4 import BeautifulSoup


link_list = []
car_list = []
min_price = 5000
max_price = 20000
car_key = 2521
total = 5
page = 0
now = 0
isWork = True

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
}

while isWork:
    page += 1
    url = f'https://cars.av.by/filter?brands[0][brand]={car_key}&price_usd[min]={min_price}&price_usd[max]={max_price}&page=' + str(page)
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    if soup.find(class_='listing__empty'):
        break

    all_cars = soup.find_all('div', class_=['listing-item', 'listing-top listing-top--color'])

    if len(all_cars) < 25:
        isWork = False

    for num in range(0, len(all_cars)):
        if now >= total:
            isWork = False
            break

        if num == 25:
            page += 1

        default_car = all_cars[num].find('div', class_=['listing-item__wrap'])

        if default_car:
            default_car_parameters = default_car.find('div', class_=['listing-item__params']).find_all('div')
            car_link = 'https://cars.av.by' + default_car.find('a', class_=['listing-item__link']).get('href')
            if car_link not in link_list:
                if default_car_parameters[1].text.split(',')[1][1:] == 'электро':
                    car = {
                        'title': default_car.find('span', class_=['link-text']).text.split(',')[0],
                        'year': default_car_parameters[0].text[:4],
                        'transmission': default_car_parameters[1].text.split(',')[0],
                        'power_reserve': default_car_parameters[1].text.split(',')[3][1:].replace('\xa0', ''),
                        # запас хода только для электричек
                        'engine': default_car_parameters[1].text.split(',')[1][1:],
                        'body': default_car_parameters[1].text.split(',')[2][1:],
                        'mileage': default_car_parameters[2].text[:-3].replace('\u2009', ''),
                        'description': default_car.find('div', class_=['listing-item__message']).text.replace('\n', ''),
                        'location': default_car.find('div', class_=['listing-item__location']).text,
                        'price': default_car.find('div', class_=['listing-item__priceusd']).text[2:-2]
                        .replace('\u2009', ''),
                        'link': car_link,
                        'img_link': default_car.find('img').get('data-src'),
                    }

                else:
                    if default_car.find('div', class_=['listing-item__message']):
                        desc = default_car.find('div', class_=['listing-item__message']).text.replace('\n', '')
                    else:
                        desc = ''

                    if len(default_car_parameters[1].text.split(',')) != 3:
                        car = {
                            'title': default_car.find('span', class_=['link-text']).text.split(',')[0],
                            'year': default_car_parameters[0].text[:4],
                            'transmission': default_car_parameters[1].text.split(',')[0],
                            'volume': default_car_parameters[1].text.split(',')[1][1:4],
                            'engine': default_car_parameters[1].text.split(',')[2][1:],
                            'body': default_car_parameters[1].text.split(',')[3][1:],
                            'mileage': default_car_parameters[2].text[:-3].replace('\u2009', ''),
                            'description': desc,
                            'location': default_car.find('div', class_=['listing-item__location']).text,
                            'price': default_car.find('div', class_=['listing-item__priceusd']).text[2:-2]
                            .replace('\u2009', ''),
                            'link': car_link,
                            'img_link': default_car.find('img').get('data-src'),
                        }

                    else:
                        car = {
                            'title': default_car.find('span', class_=['link-text']).text.split(',')[0],
                            'year': default_car_parameters[0].text[:4],
                            'transmission': default_car_parameters[1].text.split(',')[0],
                            'volume': '',
                            'engine': default_car_parameters[1].text.split(',')[1][1:],
                            'body': default_car_parameters[1].text.split(',')[2][1:],
                            'mileage': default_car_parameters[2].text[:-3].replace('\u2009', ''),
                            'description': desc,
                            'location': default_car.find('div', class_=['listing-item__location']).text,
                            'price': default_car.find('div', class_=['listing-item__priceusd']).text[2:-2]
                            .replace('\u2009', ''),
                            'link': car_link,
                            'img_link': default_car.find('img').get('data-src'),
                        }

                car_list.append(car)
                now += 1

        else:
            car_link = 'https://cars.av.by' + all_cars[num].find('a', class_=['listing-top__title-link']).get('href')
            if car_link not in link_list:
                top_car_parameters = all_cars[num].find('div', class_=['listing-top__params']).text.split(',')
                car = {
                    'title': all_cars[num].find('span', class_=['link-text']).text.split(',')[0],
                    'year': top_car_parameters[0][:4],
                    'transmission': top_car_parameters[1].split(',')[0][1:],
                    'volume': top_car_parameters[2][1:4],
                    'engine': top_car_parameters[3][1:],
                    'body': top_car_parameters[4][1:],
                    'mileage': top_car_parameters[5][:-3].replace('\u2009', ''),
                    'description': all_cars[num].find('div', class_=['listing-top__message']).text.replace('\n', ''),
                    'location': all_cars[num].find('div', class_=['listing-top__info-location']).text,
                    'price': all_cars[num].find('div', class_=['listing-top__price-usd']).text[2:-2].replace('\u2009', ''),
                    'link': car_link,
                    'img_link': all_cars[num].find('img').get('data-src'),
                }
                car_list.append(car)
                now += 1

for car in car_list:
    print(car['img_link'])