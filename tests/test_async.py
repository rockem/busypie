import asyncio

import pytest

from busypie import wait, SECOND


@pytest.fixture
def sleeper():
    yield Sleeper()


@pytest.mark.asyncio
async def test_wait_until_done(sleeper):
    await asyncio.gather(
        wait_until_awake(sleeper),
        sleeper.sleep_for_a_bit())


@pytest.mark.asyncio
async def test_wait_during_not_done(sleeper):
    await asyncio.gather(
        wait_during_sleep(sleeper),
        sleeper.sleep_for_a_bit())


class Sleeper:
    def __init__(self):
        self.awake = False

    async def sleep_for_a_bit(self):
        await asyncio.sleep(0.5)
        self.awake = True


async def wait_until_awake(sleeper):
    await wait().at_most(0.6, SECOND).until_async(lambda: sleeper.awake)
    assert sleeper.awake


async def wait_during_sleep(sleeper):
    await wait().at_most(0.6, SECOND).during_async(lambda: not sleeper.awake)
    assert sleeper.awake
