import requests
from bs4 import BeautifulSoup
import csv

"""Образец персера, подходит для сайтов hh.ru и zarplata.ru (без авторизации)"""

headers = {
    'User-Agent': 'Firefox/99.0'
}

URL = 'ссылка с поисковым запросом'

r = requests.get(URL, headers=headers)
print(r.status_code)
src = r.text

"""записываем все, что нашли в файл (на всякий случай, чтоб сервер не отказал, если будет много запросов)"""
with open('index.html', 'w') as file:
    file.write(src)

"""Читаем файл"""
with open('index.html') as file:
    src = file.read()

"""Находим все ссылки на резюме на странице, переходим по каждой, вытаскивыем инфу со страницы самого резюме. 
   Для примера вытакскиваем пол и возраст, т.к. фио и контакты недоступны без авторизации и оплаты"""
soup = BeautifulSoup(src, 'lxml')
all_resume_links = soup.find_all(class_='serp-item__title')

for el in all_resume_links:
    title = el.text
    link = 'https://hh.ru/'+el.get('href')  #или link = 'https://hr.zarplata.ru/'+el.get('href')
    req = requests.get(url=link, headers=headers)
    rest = req.text

    soup = BeautifulSoup(rest, 'lxml')
    res_data = soup.find('p').find_all('span')
    sex = res_data[0].text
    if len(res_data) > 3:
        age = res_data[2].text
    else:
        age = None

        """записываем в файл csv данные"""
    with open('data/result.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                title,
                sex,
                age,
                link
            )
        )
