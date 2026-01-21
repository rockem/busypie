import pytest

from busypie.time import time_value_operator


def test_fail_on_none_valid_time_value():
    with pytest.raises(ValueError):
        time_value_operator("string")  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        time_value_operator(None)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        time_value_operator(-2)


def test_fail_on_none_valid_time_unit():
    with pytest.raises(ValueError):
        time_value_operator(2, None)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        time_value_operator(2, -3)
