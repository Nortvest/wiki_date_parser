import re
from typing import Generator

import requests
from bs4 import BeautifulSoup
from razdel import sentenize

from date_finder import find_dates
from date_finder.rule.rules import Date


class WikiDateParser:
    def __init__(self, wiki_url: str):
        assert 'ru.wikipedia.org' in wiki_url, '"WikiDateParser" accepts only pages from Wikipedia'

        self.url = wiki_url
        self.session = requests.session()

    def __get_clear_text_from_page(self) -> list[str]:
        """Парсит страницу википедии и возвращает список параграфов"""
        response = self.session.get(self.url)

        soup = BeautifulSoup(response.text, 'lxml')
        main_block = soup.find('div', id='mw-content-text').find('div', class_='mw-parser-output')

        texts = []
        for p in main_block.find_all('p'):
            text = p.text.strip()

            # Удаление из текста сносок типа: [3], [8], [n]
            texts.append(re.sub(r'\[\d+\]', '', text))

        return texts

    def get_dates_iter(self) -> Generator[Date, str]:
        """Проходится по каждому пораграфу, делит их на предложения и находит даты"""
        for text in self.__get_clear_text_from_page():
            sentences = [_.text for _ in sentenize(text)]
            for sent in sentences:
                dates, string = find_dates(sent)
                if dates:
                    yield dates, string

    def get_dates(self) -> list[Date, str]:
        """Проходится по каждому пораграфу, делит их на предложения и находит даты"""
        return list(self.get_dates_iter())


if __name__ == '__main__':
    url = 'https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F'
    wiki_date_parser = WikiDateParser(url)
    print(*wiki_date_parser.get_dates(), sep='\n')
