import re

import requests
from bs4 import BeautifulSoup

from date_finder import find_dates


URL = 'https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F'
response = requests.get(URL)

soup = BeautifulSoup(response.text, 'lxml')
main_block = soup.find('div', id='mw-content-text').find('div', class_='mw-parser-output')

for p in main_block.find_all('p'):
    text = p.text.strip()

    # Удаление из текста сносок типа: [8], [n]
    text = re.sub(r'\[\d+\]', '', text)

    find_dates(text)

    # Добавить:
    # 1) Печечисления (через "," и "и")
    # 2) Периуды (через "-" и "с ... до\по ...") (По настоящее время)
    # 3) Слайсы есть только для годов и месяцев. (дни)
