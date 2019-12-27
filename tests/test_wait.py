from contextlib import contextmanager
from threading import Thread
from time import sleep

import pytest

from busypie import wait, wait_at_most, ConditionTimeoutError, \
    FIVE_HUNDRED_MILLISECONDS, MILLISECOND, given, ONE_HUNDRED_MILLISECONDS


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
    with pytest.raises(ConditionTimeoutError):
        wait_at_most(100, MILLISECOND).until(lambda: 'Pizza' == 'Pie')


def test_wait_until_condition_fail():
    with assert_countdown_starting_from(2) as c:
        wait().during(lambda: not c.done)


@pytest.mark.timeout(0.4)
def test_allow_to_start_with_given():
    with assert_countdown_starting_from(1) as c:
        given().wait().until(lambda: c.done)
    with pytest.raises(ConditionTimeoutError):
        given().wait_at_most(ONE_HUNDRED_MILLISECONDS).until(lambda: False)


class CountDown:
    done = False

    def start_from(self, start):
        Thread(target=self._update_after, args=(start,)).start()

    def _update_after(self, start):
        for i in range(start, 0, -1):
            sleep(0.1)
        self.done = True
