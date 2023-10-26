from yargy.predicates.bank import activate
from yargy.predicates import normalized

from .settings import MONTH_NAME_LIST


def handler_month_name(month_name):
    for normalized_month_name in activate(normalized(month_name)).value:
        if normalized_month_name in MONTH_NAME_LIST:
            return MONTH_NAME_LIST.index(normalized_month_name) + 1
