import asyncio
from functools import partial

import pytest

from busypie import ConditionTimeoutError, wait, ONE_HUNDRED_MILLISECONDS
from tests.sleeper import assert_done_after, AsyncSleeper


def test_timeout_when_not_asserted_in_time():
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(ONE_HUNDRED_MILLISECONDS).until_asserted(_failed_assertion)


def test_wait_for_assertion_to_pass():
    with assert_done_after(seconds=0.3) as c:
        wait().until_asserted(partial(_assert_is_done, c))


@pytest.mark.asyncio
async def test_await_for_assertion_to_pass():
    sleeper = AsyncSleeper()
    await asyncio.gather(
        _wait_until_awake(sleeper),
        sleeper.sleep_for_a_bit())


@pytest.mark.asyncio
async def test_fail_await_when_not_asserted_in_time():
    with pytest.raises(ConditionTimeoutError):
        await asyncio.gather(wait().at_most(ONE_HUNDRED_MILLISECONDS).until_asserted_async(_failed_assertion))


def test_retrieve_assertion_error_as_cause_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait().at_most(ONE_HUNDRED_MILLISECONDS).until_asserted(_failed_assertion)

    assert isinstance(e.value.__cause__, AssertionError)


def _failed_assertion():
    assert 1 == 2


def _assert_is_done(sleeper):
    assert sleeper.done


async def _wait_until_awake(sleeper):
    await wait() \
        .at_most(AsyncSleeper.SLEEP_DURATION + 0.1) \
        .until_asserted_async(partial(_assert_sleeper_is_awake, sleeper))
    assert sleeper.awake


def _assert_sleeper_is_awake(sleeper):
    assert sleeper.awake
