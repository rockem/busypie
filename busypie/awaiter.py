import asyncio
import time
from functools import partial
from typing import Any, Callable, Optional

import busypie
from busypie.condition import Condition
from busypie.func import describe
from busypie.types import Checker, ConditionEvaluator


class AsyncConditionAwaiter:
    def __init__(self, condition: 'Condition', evaluator_checker: Checker) -> None:
        self._condition = condition
        self._evaluator_check = evaluator_checker
        self._validate_condition()
        self._last_error: Optional[Exception] = None

    def _validate_condition(self):
        if self._condition.poll_delay > self._condition.max_wait_time:
            raise ValueError('Poll delay should be shorter than maximum wait constraint')
        if self._condition.min_wait_time >= self._condition.max_wait_time:
            raise ValueError('at least should be shorter than maximum wait constraint')

    async def wait_for(self, evaluator: ConditionEvaluator) -> Any:
        start_time = time.time()
        time_bounds_checker = partial(self._validate_wait_bounds, evaluator, start_time)
        await asyncio.sleep(self._condition.poll_delay)
        while True:
            try:
                result = await self._evaluator_check(evaluator)
                if result:
                    time_bounds_checker(self.is_under_min_wait_time)
                    return result
            except Exception as e:
                self._raise_exception_if_not_ignored(e)
                self._last_error = e
            time_bounds_checker(self.is_max_wait_time_passed)
            await asyncio.sleep(self._condition.poll_interval)

    def _validate_wait_bounds(self, condition_evaluator: ConditionEvaluator, start_time: float,
                              constraint: Callable[[float], bool]):
        execution_time = time.time() - start_time
        if constraint(execution_time):
            raise busypie.ConditionTimeoutError(
                self._describe(condition_evaluator), self._condition.max_wait_time) from self._last_error

    def _describe(self, condition_evaluator: ConditionEvaluator) -> str:
        return self._condition.description or describe(condition_evaluator)

    def is_under_min_wait_time(self, execute_time: float):
        return execute_time <= self._condition.min_wait_time

    def _raise_exception_if_not_ignored(self, e: Exception):
        ignored_exceptions = self._condition.ignored_exceptions
        if ignored_exceptions is None or \
                (ignored_exceptions and e.__class__ not in ignored_exceptions):
            raise e

    def is_max_wait_time_passed(self, execute_time: float):
        return execute_time > self._condition.max_wait_time


class ReturnOnTimeoutAwaiter:

    def __init__(self, awaiter, condition: 'Condition'):
        self._awaiter = awaiter
        self._condition = condition

    async def wait_for(self, evaluator: ConditionEvaluator) -> Any:
        try:
            return await self._awaiter.wait_for(evaluator)
        except ConditionTimeoutError as cte:
            if self._condition.return_on_timeout:
                return False
            raise cte


class ConditionTimeoutError(Exception):
    def __init__(self, description: str, max_wait_time: float):
        super(ConditionTimeoutError, self).__init__("Failed to meet condition of [{}] within {} seconds"
                                                    .format(description, max_wait_time))
        self.description = description
