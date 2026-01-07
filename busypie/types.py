from typing import Any, Callable

ConditionEvaluator = Callable[[], Any]

Checker = Callable[[ConditionEvaluator], Any]
