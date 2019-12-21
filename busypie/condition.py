import time
from time import sleep

from busypie.errors import ConditionTimeoutError
from busypie.durations import SECOND

_DEFAULT_MAX_WAIT_TIME = 10 * SECOND


class ConditionBuilder:

    def __init__(self):
        self.wait_time_in_secs = _DEFAULT_MAX_WAIT_TIME

    def at_most(self, value, unit=SECOND):
        self.wait_time_in_secs = value * unit
        return self

    def until(self, func):
        start_time = time.time()
        while True:
            if func():
                break
            if (time.time() - start_time) > self.wait_time_in_secs:
                raise ConditionTimeoutError(f"Failed to meet condition of {func.__name__} within 10 seconds")
            sleep(0.01)
