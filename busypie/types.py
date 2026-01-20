from typing import Any, Callable, Coroutine

ConditionEvaluator = Callable[[], Any]

Checker = Callable[[ConditionEvaluator], Coroutine[Any, Any, Any]]
