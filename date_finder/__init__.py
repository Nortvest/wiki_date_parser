from .rule.rules import PARSER
from .settings import Range
from .handlers import handler_correct_slice_day


def find_dates(text: str) -> tuple[list, str]:
    dates = []
    for date in PARSER.findall(text):
        if isinstance(date.fact.day, Range) and date.fact.month and date.fact.year:
            dates.append(handler_correct_slice_day(date.fact))
        else:
            dates.append(date.fact)

    return dates, text
