from yargy.rule import Rule
from yargy import rule, and_, or_, Parser
from yargy.interpretation import fact
from yargy.predicates import gte, lte, eq, caseless, normalized, dictionary

from loguru import logger
from razdel import sentenize

from .handlers import (handler_month_name,
                       handler_slice_month,
                       handler_slice_year)
from .settings import MONTH_NAME_LIST, ROMAN_CHAR_DICT
from .rule_slices import FIRST_HALF, SECOND_HALF, HALF


Date = fact(
    'Date',
    ['day', 'month', 'year']
)

SEPARATOR = dictionary({'-', '.', ','})

MONTHS = dictionary(MONTH_NAME_LIST)
DAY = and_(gte(1), lte(31)).interpretation(Date.day.custom(int))
YEAR = and_(gte(250), lte(2100)).interpretation(Date.year.custom(int))


def get_date_numerical() -> Rule:
    """
    Даты типа: "yyyy.mm.dd" и "dd.mm.yyyy
    """
    month_numerical = and_(gte(1), lte(12)).interpretation(Date.month)

    return rule(or_(
        rule(
            YEAR,
            SEPARATOR.optional(),
            month_numerical,
            SEPARATOR.optional(),
            DAY
        ),
        rule(
            DAY,
            SEPARATOR.optional(),
            month_numerical,
            SEPARATOR.optional(),
            YEAR
        ),
    ))


def get_date_string() -> Rule:
    """
    Даты типа: "yyyy год." и "dd mmmm yyyy год."
    """

    month_name = MONTHS.interpretation(
        Date.month.custom(handler_month_name)
    )

    year_words = or_(
        rule(caseless('г'), eq('.').optional()),
        rule(normalized('год'))
    )

    year_only = rule(
        or_(
            FIRST_HALF,
            SECOND_HALF,
            HALF
        ).optional().interpretation(
            Date.month.custom(handler_slice_month)
        ),
        YEAR.interpretation(Date.year),
        year_words,
    ).interpretation(
        Date
    )

    return or_(
        year_only,
        rule(  # Скобки разрешают даты типа: "(2 ноября) 1721 года" и "(14) сентября 1917 года"
            eq('(').optional(),
            DAY.optional(),
            eq(')').optional(),
            month_name,
            eq(')').optional(),
            SEPARATOR.optional(),
            YEAR.optional(),
            year_words.optional()
        ),
    )


def get_century() -> Rule:
    """
    Даты типа: handlers.Range(yyyy, yyyy)

    Переводит века в года. Учитывая контекст.

    Примеры:
    "В начале XX века" -> Range(1900, 1950)
    "Во второй половине XX века" -> Range(1950, 2000)
    "В середине XX века" -> Range(1930, 1970)

    """
    SliceCentury = fact(
        'SliceCentury',
        ['slice', 'century']
    )

    century_words = or_(caseless('в'), normalized('век'))
    roman_char = rule(dictionary(ROMAN_CHAR_DICT.keys()))
    arabic_char = and_(
        gte(1),
        lte(25)
    ).interpretation(Date.year.custom(int))

    century = rule(
        or_(
            FIRST_HALF,
            SECOND_HALF,
            HALF
        ).optional().interpretation(
            SliceCentury.slice
        ),
        or_(
            roman_char,
            arabic_char
        ).interpretation(
            SliceCentury.century
        )
    ).interpretation(
        SliceCentury
    ).interpretation(
        Date.year.custom(handler_slice_year)
    )

    return rule(
        century,
        century_words
    )


def get_full_date_rule() -> Rule:
    return or_(
        get_date_numerical(),
        get_date_string(),
        get_century()
    ).interpretation(
        Date
    )


PARSER = Parser(get_full_date_rule())


def find_dates(text: str):
    sentences = [_.text for _ in sentenize(text)]
    for sent in sentences:
        dates = [_.fact for _ in PARSER.findall(sent)]
        if dates:
            logger.success(f'{dates} | {sent}')
        else:
            logger.info(f'| {sent}')
