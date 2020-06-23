import asyncio
import inspect
import re
import time
from functools import partial

import busypie


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
        is_func_async = self._is_async(func)
        while True:
            try:
                if await self._perform_func_check(func, is_func_async):
                    break
            except Exception as e:
                self._raise_exception_if_not_ignored(e)
            self._validate_wait_constraint(func, start_time)
            await asyncio.sleep(self._condition.poll_interval)

    def _is_async(self, func):
        return inspect.iscoroutinefunction(self._unpartial(func))

    def _unpartial(self, func):
        while isinstance(func, partial):
            func = func.func
        return func

    async def _perform_func_check(self, func, is_func_async):
        return (is_func_async and await self._func_check(func)) \
            or (not is_func_async and self._func_check(func))

    def _raise_exception_if_not_ignored(self, e):
        ignored_exceptions = self._condition.ignored_exceptions
        if ignored_exceptions is None or \
                (ignored_exceptions and e.__class__ not in ignored_exceptions):
            raise e

    def _validate_wait_constraint(self, condition_func, start_time):
        if (time.time() - start_time) > self._condition.wait_time_in_secs:
            raise busypie.ConditionTimeoutError(
                self._condition.description or self._describe(condition_func), self._condition.wait_time_in_secs)

    def _describe(self, func):
        if self._is_a_lambda(func):
            return self._content_of(func)
        return self._unpartial(func).__name__

    def _is_a_lambda(self, f):
        lambda_template = lambda: 0  # noqa: E731
        return isinstance(f, type(lambda_template)) and \
            f.__name__ == lambda_template.__name__

    def _content_of(self, lambda_func):
        source_line = inspect.getsource(lambda_func)
        r = re.search(r'lambda:\s*(.+)\s*\)', source_line)
        return r.group(1)


class ConditionTimeoutError(Exception):
    def __init__(self, description, wait_time_in_secs):
        super(ConditionTimeoutError, self).__init__("Failed to meet condition of [{}] within {} seconds"
                                                    .format(description, wait_time_in_secs))
        self.description = description
