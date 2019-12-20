import pytest

from busypie import wait, ConditionTimeoutError


def test_ignore_when_condition_passed():
    try:
        wait().until(lambda: 1 == 1)
    except ConditionTimeoutError:
        pytest.fail("Failed on timeout on fulfilled condition")

