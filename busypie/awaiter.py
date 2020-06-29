import asyncio

import busypie
import time
from busypie.func import is_async, describe


class AsyncConditionAwaiter:
    def __init__(self, condition, func_checker):
        self._condition = condition
        self._func_check = func_checker
        self._validate_condition()

    def _validate_condition(self):
        if self._condition.poll_delay > self._condition.wait_time_in_secs:
            raise ValueError('Poll delay should be shorter than maximum wait constraint')

    async def wait_for(self, func):
        start_time = time.time()
        await asyncio.sleep(self._condition.poll_delay)
        is_func_async = is_async(func)
        while True:
            try:
                result = await self._perform_func_check(func, is_func_async)
                if result:
                    return result
            except Exception as e:
                self._raise_exception_if_not_ignored(e)
            self._validate_wait_constraint(func, start_time)
            await asyncio.sleep(self._condition.poll_interval)

    async def _perform_func_check(self, func, is_func_async):
        if is_func_async:
            return await self._func_check(func)
        else:
            return self._func_check(func)

    def _raise_exception_if_not_ignored(self, e):
        ignored_exceptions = self._condition.ignored_exceptions
        if ignored_exceptions is None or \
                (ignored_exceptions and e.__class__ not in ignored_exceptions):
            raise e

    def _validate_wait_constraint(self, condition_func, start_time):
        if (time.time() - start_time) > self._condition.wait_time_in_secs:
            raise busypie.ConditionTimeoutError(
                self._condition.description or describe(condition_func), self._condition.wait_time_in_secs)


class ConditionTimeoutError(Exception):
    def __init__(self, description, wait_time_in_secs):
        super(ConditionTimeoutError, self).__init__("Failed to meet condition of [{}] within {} seconds"
                                                    .format(description, wait_time_in_secs))
        self.description = description
