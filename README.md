# Russian Wikipedia Date Parser.

Developed using: Yargy: https://github.com/natasha/yargy

## Usage
``` python
>>> url = 'https://ru.wikipedia.org/wiki/Россия'
>>> wiki_date_parser = WikiDateParser(url)
>>> print(*wiki_date_parser.get_dates(), sep='\n')
[
    ([Date(day=16, month=1, year=2020)], 'C 16 января 2020 года в должности председателя правительства находится Михаил Мишустин.')
    ...
    ([Date(day=None, month=None, year=1904)], 'В 1904 году начинается Русско-японская война.')
]
>>>
>>>
>>> wiki_date_parser.get_dates_iter()
<generator object WikiDateParser.get_dates_iter at 0x0000000000000001>
```

## Opportunities
__WikiDateParser__ can parse many different date patterns.<br>
*Examples:*
- [x] Base date
  - 01.01.2020
  - 08.09.1998
  - 2020.01.01
  - 1998.09.08
- [x] String date
  - 1241 году
  - Июль 2023 года
  - 13 ноября 2021 года
- [x] Сentury
  - XI век
  - VIII в
  - 21 век
- [x] Slice
  - В конце ноября
  - В начале XIX века
  - Середина 1999 года
  - Вторая половина августа 2000 года
- [x] Periods
  - XI - X век
  - май - август 1861 года
  - С 12 до 14 марта 2023 года
  - Начиная с 1939 и вплоть до 1945 года