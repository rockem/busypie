from busypie.durations import SECOND
from busypie.condition import ConditionBuilder


def wait():
    return ConditionBuilder()


def wait_at_most(value, unit=SECOND):
    return wait().at_most(value, unit)


def given():
    return ConditionBuilder()
