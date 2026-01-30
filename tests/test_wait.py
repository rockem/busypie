import asyncio

import pytest

from backports.asyncio import run
from busypie import FIVE_HUNDRED_MILLISECONDS, MILLISECOND, ConditionTimeoutError, wait
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


def test_return_on_timeout():
    assert (
        wait().at_most(100 * MILLISECOND).return_on_timeout().until(lambda: 2 == 3)
        is False
    )


def test_raise_given_condition_invoked_before_at_least():
    with pytest.raises(ConditionTimeoutError):
        with assert_done_after(0.4) as c:
            wait().at_least(0.6).until(lambda: c.done)


def test_at_least_timeout_message():
    with pytest.raises(ConditionTimeoutError) as exc_info:
        wait().at_least(0.5).until(lambda: True)
    assert "0.5" in str(exc_info.value)
