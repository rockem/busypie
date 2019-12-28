import time
from copy import deepcopy
from time import sleep

import busypie
from busypie.durations import SECOND, ONE_HUNDRED_MILLISECONDS

DEFAULT_MAX_WAIT_TIME = 10 * SECOND
DEFAULT_POLL_INTERVAL = ONE_HUNDRED_MILLISECONDS
DEFAULT_POLL_DELAY = ONE_HUNDRED_MILLISECONDS


class ConditionBuilder:

    def __init__(self, condition=None):
        self._condition = Condition() if condition is None else condition
        self.wait_at_most = self.at_most

    def at_most(self, value, unit=SECOND):
        self._condition.wait_time_in_secs = value * unit
        return self._new_builder_with_cloned_condition()

    def _new_builder_with_cloned_condition(self):
        return ConditionBuilder(deepcopy(self._condition))

    def ignore_exceptions(self, *excludes):
        self._condition.ignored_exceptions = excludes
        return self._new_builder_with_cloned_condition()

    def wait(self):
        return self._new_builder_with_cloned_condition()

    def poll_interval(self, value, unit=SECOND):
        self._condition.poll_interval = value * unit
        return self._new_builder_with_cloned_condition()

    def poll_delay(self, value):
        self._condition.poll_delay = value
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
            self.poll_interval == other.poll_interval


class ConditionAwaiter:
    def __init__(self, condition, func_checker):
        self._condition = condition
        self._func_check = func_checker

    def wait_for(self, func):
        start_time = time.time()
        sleep(self._condition.poll_delay)
        while True:
            try:
                if self._func_check(func):
                    break
            except Exception as e:
                self._raise_exception_if_not_ignored(e)
            self._validate_wait_constraint(func.__name__, start_time)
            sleep(self._condition.poll_interval)

    def _raise_exception_if_not_ignored(self, e):
        ignored_exceptions = self._condition.ignored_exceptions
        if ignored_exceptions is None or \
                (ignored_exceptions and e.__class__ not in ignored_exceptions):
            raise e

    def _validate_wait_constraint(self, func_name, start_time):
        if (time.time() - start_time) > self._condition.wait_time_in_secs:
            raise busypie.ConditionTimeoutError("Failed to meet condition of {} within {} seconds"
                                                .format(func_name, self._condition.wait_time_in_secs))


class ConditionTimeoutError(Exception):
    pass
