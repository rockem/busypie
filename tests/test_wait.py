from contextlib import contextmanager
from threading import Thread
from time import sleep

import pytest

from busypie import wait, ConditionTimeoutError, \
    FIVE_HUNDRED_MILLISECONDS, MILLISECOND, set_default_timeout


def test_wait_until_condition_passed():
    with assert_countdown_starting_from(3) as c:
        wait().until(lambda: c.done)


@contextmanager
def assert_countdown_starting_from(start):
    countdown = CountDown()
    countdown.start_from(start)
    yield countdown
    assert countdown.done


@pytest.mark.timeout(1)
def test_timeout_when_condition_did_not_meet_in_time():
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(FIVE_HUNDRED_MILLISECONDS).until(lambda: 1 == 2)
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(100, MILLISECOND).until(lambda: False)


def test_wait_until_condition_fail():
    with assert_countdown_starting_from(2) as c:
        wait().during(lambda: not c.done)


@pytest.mark.timeout(0.7)
def test_set_default_timeout():
    set_default_timeout(500, MILLISECOND)
    with pytest.raises(ConditionTimeoutError):
        wait().until(lambda: 1 == 2)


class CountDown:
    done = False

    def start_from(self, start):
        Thread(target=self._update_after, args=(start,)).start()

    def _update_after(self, start):
        for i in range(start, 0, -1):
            sleep(0.1)
        self.done = True
