import pytest

from busypie import MILLISECOND, ONE_SECOND, ConditionTimeoutError, wait


def test_should_ignore_all_exceptions():
    with pytest.raises(ConditionTimeoutError):
        wait().ignore_exceptions().at_most(300, MILLISECOND).until(
            raise_zero_division_error
        )


def test_fail_on_exception_if_not_ignored():
    with pytest.raises(ZeroDivisionError):
        wait().at_most(ONE_SECOND).until(raise_zero_division_error)


def test_fail_on_exception_if_not_specified():
    with pytest.raises(ZeroDivisionError):
        wait().ignore_exceptions(AttributeError).at_most(ONE_SECOND).until(
            raise_zero_division_error
        )
    with pytest.raises(ConditionTimeoutError):
        wait().ignore_exceptions(AttributeError, ZeroDivisionError).at_most(
            200, MILLISECOND
        ).until(raise_zero_division_error)


def test_retrieve_cause_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait().ignore_exceptions().at_most(100, MILLISECOND).until(
            raise_zero_division_error
        )

    assert isinstance(e.value.__cause__, ZeroDivisionError)


def raise_zero_division_error():
    raise ZeroDivisionError()
