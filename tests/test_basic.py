from threading import Thread
from time import sleep

import pytest

from busypie import wait, ConditionTimeoutError, FIVE_HUNDRED_MILLISECONDS, MILLISECOND
from core import wait_at_most


def test_wait_until_condition_passed():
    countdown = CountDown()
    countdown.start_from(3)
    wait().until(lambda: countdown.done)
    assert countdown.done


@pytest.mark.timeout(1)
def test_fail_when_condition_did_not_meet_in_time():
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(FIVE_HUNDRED_MILLISECONDS).until(lambda: 1 == 2)
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(100, MILLISECOND).until(lambda: False)
    with pytest.raises(ConditionTimeoutError):
        wait_at_most(100, MILLISECOND).until(lambda: 'Pizza' == 'Pie')


class CountDown:
    done = False

    def start_from(self, start):
        Thread(target=self._update_after, args=(start,)).start()

    def _update_after(self, start):
        for i in range(start, 0):
            sleep(0.1)
        self.done = True
