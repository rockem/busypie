from typing import Callable

ConditionCallback = Callable[[], any]

Checker = Callable[[ConditionCallback], any]

