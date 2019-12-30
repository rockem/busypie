from copy import deepcopy
from functools import partial

from busypie.awaiter import ConditionAwaiter
from busypie.durations import SECOND, ONE_HUNDRED_MILLISECONDS

DEFAULT_MAX_WAIT_TIME = 10 * SECOND
DEFAULT_POLL_INTERVAL = ONE_HUNDRED_MILLISECONDS
DEFAULT_POLL_DELAY = ONE_HUNDRED_MILLISECONDS


class ConditionBuilder:

    def __init__(self, condition=None):
        self._condition = Condition() if condition is None else condition
        self._create_time_based_functions()

    def _create_time_based_functions(self):
        self.at_most = partial(self._time_property, name='wait_time_in_secs')
        self.wait_at_most = self.at_most
        self.poll_delay = partial(self._time_property, name='poll_delay')
        self.poll_interval = partial(self._time_property, name='poll_interval')

    def _time_property(self, value, unit=SECOND, name=None):
        self._validate_time_and_unit(value, unit)
        setattr(self._condition, name, value * unit)
        return self._new_builder_with_cloned_condition()

    def _validate_time_and_unit(self, value, unit):
        self._validate_positive_number(value, 'Time value of {} is not allowed')
        self._validate_positive_number(unit, 'Unit value of {} is not allowed')

    def _validate_positive_number(self, value, message):
        if value is None or value < 0:
            raise ValueError(message.format(value))

    def _new_builder_with_cloned_condition(self):
        return ConditionBuilder(deepcopy(self._condition))

    def ignore_exceptions(self, *excludes):
        self._condition.ignored_exceptions = excludes
        return self._new_builder_with_cloned_condition()

    def wait(self):
        return self._new_builder_with_cloned_condition()

    def until(self, func):
        ConditionAwaiter(
            condition=self._condition,
            func_checker=lambda f: f()).wait_for(func)

    def during(self, func):
        ConditionAwaiter(
            condition=self._condition,
            func_checker=lambda f: not f()).wait_for(func)

    def __eq__(self, other):
        if not isinstance(other, ConditionBuilder):
            return False
        return self._condition == other._condition


class ArgumentError(Exception):
    pass


class Condition:
    wait_time_in_secs = DEFAULT_MAX_WAIT_TIME
    ignored_exceptions = None
    poll_interval = DEFAULT_POLL_INTERVAL
    poll_delay = DEFAULT_POLL_DELAY

    def __eq__(self, other):
        if not isinstance(other, Condition):
            return False
        return self.wait_time_in_secs == other.wait_time_in_secs and \
            self.ignored_exceptions == other.ignored_exceptions and \
            self.poll_interval == other.poll_interval and \
            self.poll_delay == other.poll_delay
