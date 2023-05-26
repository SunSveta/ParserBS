import requests
from bs4 import BeautifulSoup
import csv

"""Если есть доступ для просмотра полного резюме, вытаскивает ФИО и номер телефона"""

headers = {
    'User-Agent': 'Firefox/99.0'
}

URL = 'https://hr.zarplata.ru/'

r = requests.get(f'{URL}search/resume?text=python&logic=normal&pos=full_text&exp_period=all_time&show_conditions=false&salary_from=&salary_to=&age_from=&age_to=&gender=unknown&order_by=relevance&search_period=0&items_on_page=50&no_magic=false', headers=headers)
print(r.status_code)
src = r.text


soup = BeautifulSoup(src, 'lxml')
all_resume_links = soup.find_all(class_='serp-item__title')

for el in all_resume_links:
    title = el.text
    link = 'https://hr.zarplata.ru/'+el.get('href')
    req = requests.get(url=link, headers=headers)
    rest = req.text

    soup = BeautifulSoup(rest, 'lxml')
    name = soup.find('div', {"class": "full-name_1yze5"}).text
    phone = soup.find('div', {'class': 'message_1Jbe_'}).find('span').text


    with open('data/ZPresult.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                name,
                title,
                phone,
                link
            )
        )
