import time
from contextlib import contextmanager

from busypie import wait, FIVE_HUNDRED_MILLISECONDS, MILLISECOND
from condition import DEFAULT_POLL_DELAY


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
    interval_recorder = IntervalRecorder()
    interval_recorder.record()
    wait().until(lambda: interval_recorder.record())
    assert DEFAULT_POLL_DELAY <= interval_recorder.interval() <= DEFAULT_POLL_DELAY + 0.01


def test_delay_with_specific_value():
    interval_recorder = IntervalRecorder()
    interval_recorder.record()
    wait().poll_delay(FIVE_HUNDRED_MILLISECONDS).until(lambda: interval_recorder.record())
    assert FIVE_HUNDRED_MILLISECONDS <= interval_recorder.interval() <= FIVE_HUNDRED_MILLISECONDS + 0.01


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
