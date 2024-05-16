import requests
import pickle
from bs4 import BeautifulSoup

cars_url = ['https://cars.av.by/bmw/5-seriya/107176248']

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
}


def connection(url):
    req = requests.get(url, headers=headers)
    src = req.text
    return BeautifulSoup(src, 'lxml')


for url in cars_url:
    soup = connection(url)
    detail_link_div = soup.find('div', class_='card__modification')
    detail_link = detail_link_div.find('a').get('href')
    car_color = soup.find('div', class_='card__description').text.split(',')[2].strip()
    description = soup.find('div', class_='card__comment-text').text
    print(description)

    new_soup = connection(detail_link)
    all_data_sections = new_soup.find_all('section', class_='modification-section')
    for i in range(len(all_data_sections)):
        section_name = all_data_sections[i].find('h2', class_='modification-section-title').text

        match(section_name):
            case 'Кузов':
                body_section = all_data_sections[i].find('dl', class_='modification-list')
                body_section_arr = []
                for body_param in body_section:
                    body_param_name = body_param.find('dt').text
                    body_param_value = body_param.find('dd').text
                    body_section_arr.append({body_param_name: body_param_value})
                db_body_section_arr = pickle.dumps(body_section_arr)

            case 'Двигатель':
                engine_section = all_data_sections[i].find('dl', class_='modification-list')
                engine_section_arr = []
                for engine_param in engine_section:
                    engine_param_name = engine_param.find('dt').text
                    engine_param_value = engine_param.find('dd').text
                    engine_section_arr.append({engine_param_name: engine_param_value})
                db_engine_section_arr = pickle.dumps(engine_section_arr)

            case 'Трансмиссия и управление':
                transmission_section = all_data_sections[i].find('dl', class_='modification-list')
                transmission_section_arr = []
                for transmission_param in transmission_section:
                    transmission_param_name = transmission_param.find('dt').text
                    transmission_param_value = transmission_param.find('dd').text
                    transmission_section_arr.append({transmission_param_name: transmission_param_value})
                db_transmission_section_arr = pickle.dumps(transmission_section_arr)

            case 'Эксплуатационные показатели':
                performance_indicators_section = all_data_sections[i].find('dl', class_='modification-list')
                performance_indicators_section_arr = []
                for performance_indicators_param in performance_indicators_section:
                    performance_indicators_param_name = performance_indicators_param.find('dt').text
                    performance_indicators_param_value = performance_indicators_param.find('dd').text
                    performance_indicators_section_arr.append({
                        performance_indicators_param_name: performance_indicators_param_value})
                db_performance_indicators_section_arr = pickle.dumps(performance_indicators_section_arr)

            case 'Подвеска и тормоза':
                suspension_and_brakes_section = all_data_sections[i].find('dl', class_='modification-list')
                suspension_and_brakes_section_arr = []
                for suspension_and_brakes_param in suspension_and_brakes_section:
                    suspension_and_brakes_param_name = suspension_and_brakes_param.find('dt').text
                    suspension_and_brakes_param_value = suspension_and_brakes_param.find('dd').text
                    suspension_and_brakes_section_arr.append({
                        suspension_and_brakes_param_name: suspension_and_brakes_param_value})
                db_suspension_and_brakes_section_arr = pickle.dumps(suspension_and_brakes_section_arr)
