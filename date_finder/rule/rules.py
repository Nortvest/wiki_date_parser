from yargy.rule import Rule
from yargy import rule, and_, or_, Parser
from yargy.interpretation import fact
from yargy.predicates import gte, lte, eq, caseless, normalized, dictionary

from ..handlers import (handler_month_name,
                       handler_slice_month,
                       handler_slice_year,
                       handler_slice_day)
from ..settings import MONTH_NAME_LIST, ROMAN_CHAR_DICT
from .rule_slices import FIRST_HALF, SECOND_HALF, HALF


Date = fact(
    'Date',
    ['day', 'month', 'year']
)

SEPARATOR = dictionary({'-', '.', ','})

DAY = and_(gte(1), lte(31)).interpretation(Date.day.custom(int))
YEAR = and_(gte(250), lte(2100)).interpretation(Date.year.custom(int))

SLICE = or_(
    FIRST_HALF,
    SECOND_HALF,
    HALF
).optional()


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

    month_name = dictionary(MONTH_NAME_LIST).interpretation(
        Date.month.custom(handler_month_name)
    )

    year_words = or_(
        rule(caseless('г'), eq('.').optional()),
        rule(normalized('год'))
    )

    # Обработка года и его частей: "В начале 2012 года", "В конце 1241 г."
    year_only = rule(
        SLICE.interpretation(
            Date.month.custom(handler_slice_month)
        ),
        YEAR,
        year_words,
    ).interpretation(
        Date
    )

    # Обработка месяца + года и его частей мемяца:
    # "В начале мая 2012 года", "В конце сентября 1241 г."
    month_and_year_date = rule(
        SLICE.interpretation(
            Date.day.custom(handler_slice_day)
        ),
        month_name,
        YEAR.optional(),
        year_words.optional()
    ).interpretation(
        Date
    )

    return or_(
        year_only,
        month_and_year_date,
        rule(  # Скобки разрешают даты типа: "(2 ноября) 1721 года" и "(14) сентября 1917 года"
            eq('(').optional(),
            DAY.optional(),
            eq(')').optional(),
            month_name,
            eq(')').optional(),
            SEPARATOR.optional(),
            YEAR.optional(),
            year_words.optional()
        )
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
        SLICE.interpretation(
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
