from builtins import Exception
from copy import deepcopy
from functools import partial
from typing import Type

from busypie import runner
from busypie.checker import check, negative_check, assert_check
from busypie.durations import ONE_HUNDRED_MILLISECONDS, SECOND
from busypie.time import time_value_operator
from busypie.types import ConditionEvaluator, Checker

DEFAULT_MAX_WAIT_TIME = 10 * SECOND
DEFAULT_POLL_INTERVAL = ONE_HUNDRED_MILLISECONDS
DEFAULT_POLL_DELAY = ONE_HUNDRED_MILLISECONDS


class ConditionBuilder:

    def __init__(self, condition: 'Condition' = None):
        self._condition = Condition() if condition is None else condition
        self._create_time_based_evaluatortions()

    def _create_time_based_evaluatortions(self):
        self.at_most = self._time_property_evaluator_for('wait_time_in_secs')
        self.wait_at_most = self.at_most
        self.poll_delay = self._time_property_evaluator_for('poll_delay')
        self.poll_interval = self._time_property_evaluator_for('poll_interval')

    def _time_property_evaluator_for(self, name: str):
        return partial(time_value_operator, visitor=partial(self._time_property, name=name))

    def _time_property(self, value: any, name: str) -> 'ConditionBuilder':
        setattr(self._condition, name, value)
        return self._new_builder_with_cloned_condition()

    def _new_builder_with_cloned_condition(self) -> 'ConditionBuilder':
        return ConditionBuilder(deepcopy(self._condition))

    def ignore_exceptions(self, *excludes: Type[Exception]) -> 'ConditionBuilder':
        self._condition.ignored_exceptions = excludes
        return self._new_builder_with_cloned_condition()

    def wait(self) -> 'ConditionBuilder':
        return self._new_builder_with_cloned_condition()

    def with_description(self, description: str) -> 'ConditionBuilder':
        self._condition.description = description
        return self._new_builder_with_cloned_condition()

    def until(self, evaluator: ConditionEvaluator) -> any:
        return runner.run(self._wait_for(evaluator, check))

    async def _wait_for(self, evaluator: ConditionEvaluator, checker: Checker):
        from busypie.awaiter import AsyncConditionAwaiter, ReturnOnTimeoutAwaiter

        return await ReturnOnTimeoutAwaiter(
            AsyncConditionAwaiter(condition=self._condition, evaluator_checker=checker),
            condition=self._condition).wait_for(evaluator)

    def during(self, evaluator: ConditionEvaluator) -> None:
        runner.run(self._wait_for(evaluator, negative_check))

    async def until_async(self, evaluator: ConditionEvaluator) -> any:
        return await self._wait_for(evaluator, check)

    async def during_async(self, evaluator: ConditionEvaluator) -> None:
        await self._wait_for(evaluator, negative_check)

    def until_asserted(self, evaluator: ConditionEvaluator) -> any:
        self._condition.append_exception(AssertionError)
        return runner.run(self._wait_for(evaluator, assert_check))

    async def until_asserted_async(self, evaluator: ConditionEvaluator) -> any:
        self._condition.append_exception(AssertionError)
        return await self._wait_for(evaluator, assert_check)

    def __eq__(self, other):
        if not isinstance(other, ConditionBuilder):
            return False
        return self._condition == other._condition

    def return_on_timeout(self) -> 'ConditionBuilder':
        self._condition.return_on_timeout = True
        return self


class Condition:
    wait_time_in_secs = DEFAULT_MAX_WAIT_TIME
    ignored_exceptions = None
    poll_interval = DEFAULT_POLL_INTERVAL
    poll_delay = DEFAULT_POLL_DELAY
    description = None
    return_on_timeout = False

    def append_exception(self, exception: Type[Exception]):
        if self.ignored_exceptions is None:
            self.ignored_exceptions = []
        self.ignored_exceptions.append(exception)

    def __eq__(self, other):
        if not isinstance(other, Condition):
            return False
        return \
            self.wait_time_in_secs == other.wait_time_in_secs and \
            self.ignored_exceptions == other.ignored_exceptions and \
            self.poll_interval == other.poll_interval and \
            self.poll_delay == other.poll_delay


set_default_timeout = partial(
    time_value_operator,
    visitor=partial(setattr, Condition, 'wait_time_in_secs'))


def reset_defaults() -> None:
    Condition.wait_time_in_secs = DEFAULT_MAX_WAIT_TIME
