from yargy.rule import Rule
from yargy import rule, and_, or_, Parser
from yargy.interpretation import fact
from yargy.predicates import gte, lte, eq, caseless, normalized, dictionary

from ..handlers import (handler_month_name,
                        handler_slice_month,
                        handler_slice_year,
                        handler_slice_day,
                        handler_int_period,
                        handler_range_period)
from ..settings import MONTH_NAME_LIST, ROMAN_CHAR_DICT
from .rule_slices import FIRST_HALF, SECOND_HALF, HALF
from .rule_periods import get_period_rule


Date = fact(
    'Date',
    ['day', 'month', 'year']
)

SEPARATOR = dictionary({'-', '.', ','})

DAY = and_(gte(1), lte(31)).interpretation(Date.day.custom(int))
YEAR = and_(gte(250), lte(2100)).interpretation(Date.year.custom(int))

SLICE_OPTIONAL = or_(
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
        or_(
            get_period_rule(YEAR).interpretation(Date.year.custom(handler_int_period)),
            rule(
                SLICE_OPTIONAL.interpretation(Date.month.custom(handler_slice_month)),
                YEAR
            ),
        ),
        year_words,
    ).interpretation(Date)

    # Обработка месяца + года и его частей мемяца:
    # "В начале мая 2012 года", "В конце сентября 1241 г."
    month_and_year_date = rule(
        or_(
            get_period_rule(month_name).interpretation(Date.month.custom(handler_int_period)),
            rule(
                SLICE_OPTIONAL.interpretation(Date.day.custom(handler_slice_day)),
                month_name
            ),
        ),
        YEAR.optional(),
        year_words.optional()
    ).interpretation(Date)

    period_days = rule(  # Периуды в днях в датах: "с 12 по 23 декабря 1243 год", "1-12 ноября 1234 года"
        get_period_rule(DAY).interpretation(Date.day.custom(handler_int_period)),
        month_name,
        SEPARATOR.optional(),
        YEAR.optional(),
        year_words.optional()
    )

    return or_(
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
        period_days,
        month_and_year_date,
        year_only
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
        SLICE_OPTIONAL.interpretation(SliceCentury.slice),
        or_(
            roman_char,
            arabic_char
        ).interpretation(SliceCentury.century)
    ).interpretation(
        SliceCentury
    ).interpretation(
        Date.year.custom(handler_slice_year)
    )

    return rule(
        or_(
            get_period_rule(century).interpretation(Date.year.custom(handler_range_period)),
            century
        ),
        century_words
    )


def get_full_date_rule() -> Rule:
    return or_(
        get_date_numerical(),
        get_date_string(),
        get_century()
    ).interpretation(Date)


PARSER = Parser(get_full_date_rule())
