from busypie.durations import SECOND
from busypie.condition import ConditionBuilder
import busypie.condition


def wait():
    return ConditionBuilder()


def wait_at_most(value, unit=SECOND):
    return wait().at_most(value, unit)


def given():
    return ConditionBuilder()


def set_default_timeout(value, unit):
    busypie.condition.set_default_timeout(value, unit)
    print("1")
