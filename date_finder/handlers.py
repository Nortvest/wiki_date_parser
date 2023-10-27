from dataclasses import dataclass

from yargy.predicates.bank import activate
from yargy.predicates import normalized

from .settings import MONTH_NAME_LIST, ROMAN_CHAR_DICT, OFFSET_CENTURY, OFFSET_DEFAULT


@dataclass
class Range:
    start: int
    end: int


def handler_month_name(month_name: str) -> int:
    for normalized_month_name in activate(normalized(month_name)).value:
        if normalized_month_name in MONTH_NAME_LIST:
            return MONTH_NAME_LIST.index(normalized_month_name) + 1


def handler_roman_century(data: 'SliceCentury') -> Range:
    roman_numeral = data.century
    slice_century = data.slice

    value = ROMAN_CHAR_DICT[roman_numeral]
    offset_start, offset_end = OFFSET_CENTURY.get(slice_century, OFFSET_DEFAULT)

    return Range(
        (value - 1) * 100 + offset_start,
        value * 100 + offset_end
    )
