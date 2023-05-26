import requests
from bs4 import BeautifulSoup
import csv

"""Если есть доступ для просмотра полного резюме, вытаскивает ФИО и номер телефона"""

headers = {
    'User-Agent': 'Firefox/99.0'
}

URL = 'https://rabota.ru/'

r = requests.get(f'{URL}v3_searchResumeByParamsResults.html?id=35157410', headers=headers)
print(r.status_code)
src = r.text

with open('index.html', 'w') as file:
    file.write(src)

with open('index.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_resume_links = soup.find_all(class_='js-follow-link-ignore box-wrapper__resume-name')

for el in all_resume_links:

    title = el.text
    link = el.get('href')

    req = requests.get(url=link, headers=headers)
    rest = req.text

    soup = BeautifulSoup(rest, 'lxml')
    name = soup.find('span', {"class": "first-letter-up"}).text
    phone = soup.find('a', {'class': 'text-black'}).text

    with open('data/RBresult.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                name,
                title,
                phone,
                link
            )
        )
