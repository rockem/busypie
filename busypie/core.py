import busypie.condition
from busypie.condition import ConditionBuilder
from busypie.durations import SECOND


def wait() -> 'ConditionBuilder':
    return ConditionBuilder()


given = wait


def wait_at_most(value: float, unit: float = SECOND) -> 'ConditionBuilder':
    return wait().at_most(value, unit)


set_default_timeout = busypie.condition.set_default_timeout

reset_defaults = busypie.condition.reset_defaults
