from dataclasses import dataclass

from yargy.predicates.bank import activate
from yargy.predicates import normalized

from .settings import Offset, MONTH_NAME_LIST, ROMAN_CHAR_DICT


@dataclass
class Range:
    start: int
    end: int


def handler_month_name(month_name: str) -> int:
    for normalized_month_name in activate(normalized(month_name)).value:
        if normalized_month_name in MONTH_NAME_LIST:
            return MONTH_NAME_LIST.index(normalized_month_name) + 1


def handler_slice_year(data: 'SliceCentury') -> Range:
    value = data.century
    slice_century = data.slice

    value = ROMAN_CHAR_DICT.get(value, value)
    offset_start, offset_end = Offset.OFFSET_YEAR.get(slice_century, Offset.OFFSET_DEFAULT_YEAR)

    return Range(
        (value - 1) * 100 + offset_start,
        value * 100 + offset_end
    )


def handler_slice_month(diapason_name: str) -> Range:
    return Range(*Offset.OFFSET_MONTH.get(diapason_name, Offset.OFFSET_DEFAULT_MONTH))
