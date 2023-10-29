from calendar import monthrange

from yargy.predicates.bank import activate
from yargy.predicates import normalized

from .settings import Offset, MONTH_NAME_LIST, ROMAN_CHAR_DICT, Range


def handler_month_name(month_name: str) -> int:
    for normalized_month_name in activate(normalized(month_name)).value:
        if normalized_month_name in MONTH_NAME_LIST:
            return MONTH_NAME_LIST.index(normalized_month_name) + 1


def handler_slice_year(slice_century: 'SliceCentury') -> Range:
    value = slice_century.century
    slice_century = slice_century.slice

    value = ROMAN_CHAR_DICT.get(value, value)
    offset_start, offset_end = Offset.OFFSET_YEAR.get(slice_century, Offset.OFFSET_DEFAULT_YEAR)

    return Range(
        (value - 1) * 100 + offset_start,
        value * 100 + offset_end
    )


def handler_slice_month(diapason_month_name: str) -> Range:
    return Range(*Offset.OFFSET_MONTH.get(diapason_month_name, Offset.OFFSET_DEFAULT_MONTH))


def handler_slice_day(diapason_day_name: str) -> Range:
    return Range(*Offset.OFFSET_DAY.get(diapason_day_name, Offset.OFFSET_DEFAULT_DAY))


def handler_correct_slice_day(date: 'Date') -> 'Date':
    _, num_days = monthrange(date.year, date.month)
    if date.day.end == Offset.OFFSET_DAY['SECOND_HALF'][1]:
        date.day.end = num_days
    return date
