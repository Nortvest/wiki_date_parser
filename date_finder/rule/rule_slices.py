from yargy import rule, or_
from yargy.predicates import normalized, eq
from yargy import interpretation as interp


FIRST_HALF = or_(
    rule(normalized('начало')),
    rule(
        or_(normalized('к'), normalized('до')),
        normalized('середина')
    ),
    rule(normalized('первая'), normalized('половина'))
).interpretation(interp.const('FIRST_HALF'))

SECOND_HALF = or_(
    rule(normalized('конец')),
    rule(
        or_(normalized('с'), normalized('после')),
        normalized('середина')
    ),
    rule(normalized('вторая'), normalized('половина'))
).interpretation(interp.const('SECOND_HALF'))

HALF = rule(
    normalized('в').optional(),
    normalized('середина')
).interpretation(interp.const('HALF'))
