from dataclasses import dataclass


MONTH_NAME_LIST = [
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь'
]

ROMAN_CHAR_DICT = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
    'XI': 11,
    'XII': 12,
    'XIII': 13,
    'XIV': 14,
    'XV': 15,
    'XVI': 16,
    'XVII': 17,
    'XVIII': 18,
    'XIX': 19,
    'XX': 20,
    'XXI': 21,
    'XXII': 22,
    'XXIII': 23,
    'XXIV': 24,
    'XXV': 25
}


@dataclass
class Range:
    start: int
    end: int


@dataclass
class Offset:
    OFFSET_DEFAULT_YEAR = (0, 0)
    OFFSET_YEAR = {
        'FIRST_HALF': (0, -50),
        'SECOND_HALF': (50, 0),
        'HALF': (30, -30),
    }

    OFFSET_DEFAULT_MONTH = (1, 12)
    OFFSET_MONTH = {
        'FIRST_HALF': (1, 6),
        'SECOND_HALF': (6, 12),
        'HALF': (3, 9),
    }

    OFFSET_DEFAULT_DAY = (1, 31)
    OFFSET_DAY = {
        'FIRST_HALF': (1, 15),
        'SECOND_HALF': (15, 31),
        'HALF': (10, 20),
    }
