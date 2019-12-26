from contextlib import contextmanager
from threading import Thread
from time import sleep

from busypie import wait


def test_wait_until_condition_passed():
    with assert_countdown_starting_from(3) as c:
        wait().until(lambda: c.done)


@contextmanager
def assert_countdown_starting_from(start):
    countdown = CountDown()
    countdown.start_from(start)
    yield countdown
    assert countdown.done


def test_wait_until_condition_fail():
    with assert_countdown_starting_from(2) as c:
        wait().during(lambda: not c.done)


class CountDown:
    done = False

    def start_from(self, start):
        Thread(target=self._update_after, args=(start,)).start()

    def _update_after(self, start):
        for i in range(start, 0, -1):
            sleep(0.1)
        self.done = True