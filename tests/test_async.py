import asyncio
from functools import partial

import pytest

from busypie import SECOND, ConditionTimeoutError, wait


@pytest.fixture
def sleeper():
    yield Sleeper()


@pytest.mark.asyncio
async def test_wait_until_done(sleeper):
    await asyncio.gather(
        wait_until_awake(sleeper),
        sleeper.sleep_for_a_bit())


@pytest.mark.asyncio
async def test_wait_with_async_condition(sleeper):
    await asyncio.gather(
        async_wait_until_awake(sleeper),
        sleeper.sleep_for_a_bit())


@pytest.mark.asyncio
async def test_wait_during_not_done(sleeper):
    await asyncio.gather(
        wait_during_sleep(sleeper),
        sleeper.sleep_for_a_bit())


@pytest.mark.asyncio
async def test_wait_fail_on_timeout(sleeper):
    with pytest.raises(ConditionTimeoutError):
        await asyncio.gather(
            async_wait_until_awake(sleeper, delay=0.6),
            sleeper.sleep_for_a_bit())


@pytest.mark.asyncio
async def test_retrieve_condition_result(sleeper):
    assert await wait().until_async(return_12) == 12


class Sleeper:
    def __init__(self):
        self.awake = False

    async def sleep_for_a_bit(self):
        await asyncio.sleep(0.5)
        self.awake = True

    async def get_awake_with_delay(self, delay_sec):
        awake = self.awake
        await asyncio.sleep(delay_sec)
        return awake


async def wait_until_awake(sleeper):
    await wait().at_most(0.6, SECOND).until_async(lambda: sleeper.awake)
    assert sleeper.awake


async def wait_during_sleep(sleeper):
    await wait().at_most(0.6, SECOND).during_async(lambda: not sleeper.awake)
    assert sleeper.awake


async def async_wait_until_awake(sleeper: Sleeper, delay=0.01):
    await wait().at_most(0.6, SECOND).until_async(partial(sleeper.get_awake_with_delay, delay))
    assert sleeper.awake


async def return_12():
    return 12
