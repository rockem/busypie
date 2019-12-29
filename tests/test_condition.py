import pytest

from busypie.condition import ConditionBuilder


def test_fail_on_none_valid_time_value():
    with pytest.raises(ValueError):
        ConditionBuilder().poll_interval(None)
    with pytest.raises(ValueError):
        ConditionBuilder().poll_delay(-2)


def test_fail_on_none_valid_time_unit():
    with pytest.raises(ValueError):
        ConditionBuilder().poll_interval(2, None)
    with pytest.raises(ValueError):
        ConditionBuilder().poll_interval(2, -3)
