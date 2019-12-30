import time
from time import sleep

import busypie


class ConditionAwaiter:
    def __init__(self, condition, func_checker):
        self._condition = condition
        self._func_check = func_checker
        self._validate_condition()

    def _validate_condition(self):
        if self._condition.poll_delay > self._condition.wait_time_in_secs:
            raise ValueError('Poll delay should be shorter than maximum wait constraint')

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
