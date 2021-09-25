import asyncio
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


class AsyncSleeper:
    SLEEP_DURATION = 0.5

    def __init__(self):
        self.awake = False

    async def sleep_for_a_bit(self):
        await asyncio.sleep(self.SLEEP_DURATION)
        self.awake = True

    async def get_awake_with_delay(self, delay_sec):
        awake = self.awake
        await asyncio.sleep(delay_sec)
        return awake
