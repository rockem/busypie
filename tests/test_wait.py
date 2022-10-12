import asyncio

import pytest

from backports.asyncio import run
from busypie import (FIVE_HUNDRED_MILLISECONDS, MILLISECOND,
                     ConditionTimeoutError, wait)
from tests.sleeper import assert_done_after


def test_wait_until_condition_passed():
    with assert_done_after(seconds=0.3) as c:
        wait().until(lambda: c.done)


def test_wait_until_condition_passed_after_using_event_loop():
    run(asyncio.sleep(0.1))
    with assert_done_after(seconds=0.3) as c:
        wait().until(lambda: c.done)


@pytest.mark.timeout(1)
def test_timeout_when_condition_did_not_meet_in_time():
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(FIVE_HUNDRED_MILLISECONDS).until(lambda: 1 == 2)
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(100, MILLISECOND).until(lambda: False)


def test_wait_until_condition_fail():
    with assert_done_after(seconds=0.2) as c:
        wait().during(lambda: not c.done)


def test_retrieve_condition_result():
    assert wait().until(lambda: 3) == 3


def test_nested_waits():
    def condition():
        return wait().until(lambda: True)

    assert wait().until(condition)


def test_wait_until_with_lambda_captures():
    c1 = 321
    c2 = 123
    assert wait().until(lambda x=c1, y=c2: x + y) == (c1 + c2)
