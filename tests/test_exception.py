import pytest

from busypie import wait, ConditionTimeoutError, MILLISECOND, ONE_SECOND


def test_should_ignore_all_exceptions():
    with pytest.raises(ConditionTimeoutError):
        wait().ignore_exceptions().at_most(200, MILLISECOND).until(raise_error)


def test_fail_on_exception_if_not_ignored():
    with pytest.raises(ZeroDivisionError):
        wait().at_most(ONE_SECOND).until(raise_error)


def raise_error():
    raise ZeroDivisionError()