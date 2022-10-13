import asyncio
from functools import partial

import pytest

from busypie import ConditionTimeoutError, wait
from tests.sleeper import AsyncSleeper


@pytest.fixture
def sleeper():
    yield AsyncSleeper()


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
        async_wait_during_sleep(sleeper),
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


async def return_12():
    return 12


async def wait_until_awake(sleeper):
    await wait().at_most(AsyncSleeper.SLEEP_DURATION + 0.1).until_async(lambda: sleeper.awake)
    assert sleeper.awake


async def async_wait_during_sleep(sleeper):
    await wait().at_most(AsyncSleeper.SLEEP_DURATION + 0.1).during_async(partial(is_asleep, sleeper))
    assert sleeper.awake


async def is_asleep(sleeper):
    return not sleeper.awake


async def async_wait_until_awake(sleeper, delay=0.01):
    await wait().at_most(AsyncSleeper.SLEEP_DURATION + 0.1).until_async(partial(sleeper.get_awake_with_delay, delay))
    assert sleeper.awake
