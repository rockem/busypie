from contextlib import contextmanager
from threading import Thread
from time import sleep


@contextmanager
def assert_done_after(seconds):
    sleeper = Sleeper()
    sleeper.sleep_for(seconds)
    yield sleeper
    assert sleeper.done


class Sleeper:
    done = False

    def sleep_for(self, start):
        Thread(target=self._wake_up_after, args=(start,)).start()

    def _wake_up_after(self, seconds):
        sleep(seconds)
        self.done = True
