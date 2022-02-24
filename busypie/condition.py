from copy import deepcopy
from functools import partial

from busypie import runner
from busypie.awaiter import AsyncConditionAwaiter
from busypie.durations import ONE_HUNDRED_MILLISECONDS, SECOND
from busypie.func import is_async
from busypie.time import time_value_operator

DEFAULT_MAX_WAIT_TIME = 10 * SECOND
DEFAULT_POLL_INTERVAL = ONE_HUNDRED_MILLISECONDS
DEFAULT_POLL_DELAY = ONE_HUNDRED_MILLISECONDS


class ConditionBuilder:

    def __init__(self, condition=None):
        self._condition = Condition() if condition is None else condition
        self._create_time_based_functions()

    def _create_time_based_functions(self):
        self.at_most = self._time_property_func_for('wait_time_in_secs')
        self.wait_at_most = self.at_most
        self.poll_delay = self._time_property_func_for('poll_delay')
        self.poll_interval = self._time_property_func_for('poll_interval')

    def _time_property_func_for(self, name):
        return partial(time_value_operator, visitor=partial(self._time_property, name=name))

    def _time_property(self, value, name):
        setattr(self._condition, name, value)
        return self._new_builder_with_cloned_condition()

    def _new_builder_with_cloned_condition(self):
        return ConditionBuilder(deepcopy(self._condition))

    def ignore_exceptions(self, *excludes):
        self._condition.ignored_exceptions = excludes
        return self._new_builder_with_cloned_condition()

    def wait(self):
        return self._new_builder_with_cloned_condition()

    def with_description(self, description):
        self._condition.description = description
        return self._new_builder_with_cloned_condition()

    def until(self, func):
        return runner.run(self._wait_for(func, self._check))

    @staticmethod
    async def _check(f):
        if is_async(f):
            return await f()
        return f()

    async def _wait_for(self, func, checker):
        return await AsyncConditionAwaiter(
            condition=self._condition,
            func_checker=checker).wait_for(func)

    def during(self, func):
        runner.run(self._wait_for(func, self._negative_check))

    @staticmethod
    async def _negative_check(f):
        if is_async(f):
            result = await f()
            return not result
        return not f()

    async def until_async(self, func):
        return await self._wait_for(func, self._check)

    async def during_async(self, func):
        await self._wait_for(func, self._negative_check)

    def until_asserted(self, func):
        self._condition.append_exception(AssertionError)
        return runner.run(self._wait_for(func, self._check_assert))

    @staticmethod
    async def _check_assert(f):
        f()
        return True

    async def until_asserted_async(self, func):
        self._condition.append_exception(AssertionError)
        await self._wait_for(func, self._check_assert)

    def __eq__(self, other):
        if not isinstance(other, ConditionBuilder):
            return False
        return self._condition == other._condition


class Condition:
    wait_time_in_secs = DEFAULT_MAX_WAIT_TIME
    ignored_exceptions = None
    poll_interval = DEFAULT_POLL_INTERVAL
    poll_delay = DEFAULT_POLL_DELAY
    description = None

    def append_exception(self, exception):
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


def reset_defaults():
    Condition.wait_time_in_secs = DEFAULT_MAX_WAIT_TIME
