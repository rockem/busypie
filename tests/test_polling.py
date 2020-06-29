from contextlib import contextmanager

import pytest

import time
from busypie import wait, FIVE_HUNDRED_MILLISECONDS, MILLISECOND, SECOND
from busypie.condition import DEFAULT_POLL_DELAY


def test_poll_with_specific_interval():
    with verify_poll_interval_is(FIVE_HUNDRED_MILLISECONDS) as verifier:
        wait().poll_interval(FIVE_HUNDRED_MILLISECONDS).until(verifier.record)
    with verify_poll_interval_is(200 * MILLISECOND) as verifier:
        wait().poll_interval(200, MILLISECOND).until(verifier.record)


@contextmanager
def verify_poll_interval_is(interval):
    polling_insights = IntervalRecorder()
    yield polling_insights
    assert abs(interval - polling_insights.interval()) <= 0.02


def test_default_delay():
    with verify_delay_is(DEFAULT_POLL_DELAY) as recorder:
        wait().until(lambda: recorder.record())


@contextmanager
def verify_delay_is(delay):
    interval_recorder = IntervalRecorder()
    interval_recorder.record()
    yield interval_recorder
    assert delay <= interval_recorder.interval() <= delay + 0.01


@pytest.mark.timeout(2)
def test_delay_with_specific_value():
    with verify_delay_is(FIVE_HUNDRED_MILLISECONDS) as recorder:
        wait().poll_delay(FIVE_HUNDRED_MILLISECONDS).until(lambda: recorder.record())
    with verify_delay_is(200 * MILLISECOND) as recorder:
        wait().poll_delay(200, MILLISECOND).until(lambda: recorder.record())


@pytest.mark.timeout(1)
def test_fail_on_delay_longer_than_max_wait_time():
    with pytest.raises(ValueError):
        wait().poll_delay(11, SECOND).until(lambda: True)


class IntervalRecorder:
    start_time = None
    _end_time = None

    def record(self):
        if self.start_time:
            self._end_time = time.time()
            return True
        self.start_time = time.time()
        return False

    def interval(self):
        return round(self._end_time - self.start_time, 4)
