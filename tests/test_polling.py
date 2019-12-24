import time
from contextlib import contextmanager

from busypie import wait, FIVE_HUNDRED_MILLISECONDS, MILLISECOND


def test_poll_with_specific_interval():
    with verify_poll_interval_is(FIVE_HUNDRED_MILLISECONDS) as verifier:
        wait().poll_interval(FIVE_HUNDRED_MILLISECONDS).until(verifier.is_done)
    with verify_poll_interval_is(200 * MILLISECOND) as verifier:
        wait().poll_interval(200, MILLISECOND).until(verifier.is_done)


@contextmanager
def verify_poll_interval_is(interval):
    interval_counter = IntervalCounter()
    yield interval_counter
    assert interval - 0.02 < interval_counter.interval() < interval + 0.02


class IntervalCounter:
    _start_time = None
    _end_time = None

    def is_done(self):
        if self._start_time:
            self._end_time = time.time()
            return True
        self._start_time = time.time()
        return False

    def interval(self):
        return self._end_time - self._start_time
