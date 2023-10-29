from loguru import logger
from razdel import sentenize

from .rules import PARSER


def find_dates(text: str):
    sentences = [_.text for _ in sentenize(text)]
    for sent in sentences:
        dates = [_.fact for _ in PARSER.findall(sent)]
        if dates:
            logger.success(f'{dates} | {sent}')
        else:
            logger.info(f'| {sent}')
