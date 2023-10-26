from yargy import rule, and_, or_, Parser
from yargy.interpretation import fact
from yargy.predicates import gte, lte, eq, caseless, normalized, dictionary

import re
from loguru import logger
from razdel import sentenize

from .handlers import handler_month_name
from .settings import MONTH_NAME_LIST


Date = fact(
    'Date',
    ['day', 'month', 'year']
)

SEPARATOR = dictionary({'-', '.', ','})
DOT = eq('.')
YEAR_WORDS = or_(caseless('г'), normalized('год'))
MONTHS_NAME = dictionary(MONTH_NAME_LIST).interpretation(
    Date.month.custom(handler_month_name)
)

DAY = and_(gte(1), lte(31)).interpretation(Date.day)
MONTH_NUMERIC = and_(gte(1), lte(12)).interpretation(Date.month)
YEAR = and_(gte(1000), lte(2100)).interpretation(Date.year)

DATE = or_(*[
    rule(
        YEAR,
        SEPARATOR.optional(),
        MONTH_NUMERIC,
        SEPARATOR.optional(),
        DAY
    ),
    rule(
        DAY,
        SEPARATOR.optional(),
        MONTH_NUMERIC,
        SEPARATOR.optional(),
        YEAR
    ),
    rule(
        YEAR,
        YEAR_WORDS,
        DOT.optional()
    ),
    rule(
        DAY.optional(),
        MONTHS_NAME,
        SEPARATOR.optional(),
        YEAR.optional(),
        YEAR_WORDS.optional(),
        DOT.optional()
    )
]).interpretation(
    Date
)

parser = Parser(DATE)


def find_dates(text: str):
        sentences = [_.text for _ in sentenize(text)]
        for sent in sentences:
            dates = [_.fact for _ in parser.findall(sent)]
            if dates:
                logger.success(f'{dates} | {sent}')
            else:
                logger.info(f'| {sent}')
