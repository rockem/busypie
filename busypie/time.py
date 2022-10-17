from numbers import Number
from typing import Callable

from busypie.durations import SECOND


def time_value_operator(value: float, unit: float = SECOND, visitor: Callable[[float], any] = None) -> any:
    _validate_time_and_unit(value, unit)
    return visitor(value * unit)


def _validate_time_and_unit(value: float, unit: float) -> None:
    _validate_positive_number(value, 'Time value of {} is not allowed')
    _validate_positive_number(unit, 'Unit value of {} is not allowed')


def _validate_positive_number(value: float, message: str) -> None:
    if value is None or not isinstance(value, Number) or value < 0:
        raise ValueError(message.format(value))
