from yargy.rule import Rule
from yargy import rule, or_
from yargy.interpretation import fact
from yargy.predicates import eq, caseless


DatePeriod = fact(
    'DatePeriod',
    ['start', 'end']
)


def get_str_period_rule(middleware: Rule) -> Rule:
    return rule(
        caseless('с').optional(),
        middleware.interpretation(DatePeriod.start),
        caseless('и').optional(),
        caseless('вплоть').optional(),
        or_(
            caseless('по'),
            caseless('до')
        ),
        middleware.interpretation(DatePeriod.end)
    )


def get_char_period_rule(middleware: Rule) -> Rule:
    return rule(
        middleware.interpretation(DatePeriod.start),
        or_(eq('-'), eq('–'), eq('—'), eq('‒'), eq('－'), eq('﹣')),
        middleware.interpretation(DatePeriod.end)
    )


def get_period_rule(middleware: Rule) -> Rule:
    return rule(
        or_(
            get_str_period_rule(middleware),
            get_char_period_rule(middleware)
        )
    ).interpretation(DatePeriod)
