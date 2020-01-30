from busypie.durations import SECOND
from busypie.condition import ConditionBuilder
import busypie.condition


def wait():
    return ConditionBuilder()


given = wait


def wait_at_most(value, unit=SECOND):
    return wait().at_most(value, unit)


set_default_timeout = busypie.condition.set_default_timeout
