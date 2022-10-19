import asyncio

import busypie
import time

from busypie.condition import Condition
from busypie.func import describe
from busypie.types import Checker, ConditionEvaluator


class AsyncConditionAwaiter:
    def __init__(self, condition: 'Condition', evaluator_checker: Checker):
        self._condition = condition
        self._evaluator_check = evaluator_checker
        self._validate_condition()
        self._last_error = None

    def _validate_condition(self):
        if self._condition.poll_delay > self._condition.wait_time_in_secs:
            raise ValueError('Poll delay should be shorter than maximum wait constraint')

    async def wait_for(self, evaluator: ConditionEvaluator) -> any:
        start_time = time.time()
        await asyncio.sleep(self._condition.poll_delay)
        while True:
            try:
                result = await self._evaluator_check(evaluator)
                if result:
                    return result
            except Exception as e:
                self._raise_exception_if_not_ignored(e)
                self._last_error = e
            self._validate_wait_constraint(evaluator, start_time)
            await asyncio.sleep(self._condition.poll_interval)

    def _raise_exception_if_not_ignored(self, e: Exception):
        ignored_exceptions = self._condition.ignored_exceptions
        if ignored_exceptions is None or \
                (ignored_exceptions and e.__class__ not in ignored_exceptions):
            raise e

    def _validate_wait_constraint(self, condition_evaluator: ConditionEvaluator, start_time: float):
        if (time.time() - start_time) > self._condition.wait_time_in_secs:
            raise busypie.ConditionTimeoutError(
                self._describe(condition_evaluator), self._condition.wait_time_in_secs) from self._last_error

    def _describe(self, condition_evaluator: ConditionEvaluator) -> str:
        return self._condition.description or describe(condition_evaluator)


class ReturnOnTimeoutAwaiter:

    def __init__(self, awaiter, condition: 'Condition'):
        self._awaiter = awaiter
        self._condition = condition

    async def wait_for(self, evaluator: ConditionEvaluator) -> any:
        try:
            return await self._awaiter.wait_for(evaluator)
        except ConditionTimeoutError as cte:
            if self._condition.return_on_timeout:
                return False
            raise cte


class ConditionTimeoutError(Exception):
    def __init__(self, description: str, wait_time_in_secs: float):
        super(ConditionTimeoutError, self).__init__("Failed to meet condition of [{}] within {} seconds"
                                                    .format(description, wait_time_in_secs))
        self.description = description
