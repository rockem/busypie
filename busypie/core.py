from busypie.durations import SECOND
from busypie.condition import ConditionBuilder


def wait():
    return ConditionBuilder()


def wait_at_most(value, unit=SECOND):
    return ConditionBuilder().at_most(value, unit)
