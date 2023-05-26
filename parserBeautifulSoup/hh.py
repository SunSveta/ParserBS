import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Firefox/99.0'
}

URL = 'https://hh.ru/'

r = requests.get(f'{URL}search/resume?text=python&area=1&isDefaultArea=true&pos=full_text&logic=normal&exp_period=all_time&ored_clusters=true&order_by=relevance&search_period=0', headers=headers)
print(r.status_code)
src = r.text


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

    with open('data/HHresult.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                title,
                sex,
                age,
                link
            )
        )
