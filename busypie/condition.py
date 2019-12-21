import time
from time import sleep

import busypie
from busypie.durations import SECOND, ONE_HUNDRED_MILLISECONDS

_DEFAULT_MAX_WAIT_TIME = 10 * SECOND


class ConditionBuilder:

    def __init__(self):
        self._condition = Condition()

    def at_most(self, value, unit=SECOND):
        self._condition.wait_time_in_secs = value * unit
        return self

    def ignore_exceptions(self):
        self._condition.ignore_all_exceptions = True
        return self

    def until(self, func):
        ConditionAwaiter(self._condition).wait_for(func)


class Condition:
    wait_time_in_secs = _DEFAULT_MAX_WAIT_TIME
    ignore_all_exceptions = False


class ConditionAwaiter:

    def __init__(self, condition):
        self._condition = condition

    def wait_for(self, func):
        start_time = time.time()
        while True:
            try:
                if func():
                    break
            except Exception as e:
                self._raise_exception_if_needed(e)
            self.validate_wait_constraint(func.__name__, start_time)
            sleep(ONE_HUNDRED_MILLISECONDS)

    def _raise_exception_if_needed(self, e):
        if not self._condition.ignore_all_exceptions:
            raise e

    def validate_wait_constraint(self, func_name, start_time):
        if (time.time() - start_time) > self._condition.wait_time_in_secs:
            raise busypie.ConditionTimeoutError("Failed to meet condition of {} within {} seconds"
                                        .format(func_name, self._condition.wait_time_in_secs))


class ConditionTimeoutError(Exception):
    pass
