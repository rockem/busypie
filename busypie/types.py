from typing import Callable

ConditionEvaluator = Callable[[], any]

Checker = Callable[[ConditionEvaluator], any]
