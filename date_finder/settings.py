MONTH_NAME_LIST = [
    'январь',
    'февраль',
    'март',
    'апрель',
    'мая',
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

OFFSET_DEFAULT = (0, 0)

OFFSET_CENTURY = {
    'FIRST_HALF': (0, -50),
    'SECOND_HALF': (50, 0),
    'HALF': (30, -30),
}

OFFSET_YEAR = {
    'FIRST_HALF': (1, 6),
    'SECOND_HALF': (6, 12),
    'HALF': (3, 9),
}

OFFSET_MONTH = {
    'FIRST_HALF': (1, 15),
    'SECOND_HALF': (15, 30),
    'HALF': (10, 20),
}
