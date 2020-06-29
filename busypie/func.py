import inspect
import re
from functools import partial


def is_async(func):
    return inspect.iscoroutinefunction(_unpartial(func))


def _unpartial(func):
    while isinstance(func, partial):
        func = func.func
    return func


def describe(func):
    if _is_a_lambda(func):
        return _content_of(func)
    return _unpartial(func).__name__


def _is_a_lambda(func):
    lambda_template = lambda: 0  # noqa: E731
    return isinstance(func, type(lambda_template)) and \
        func.__name__ == lambda_template.__name__


def _content_of(lambda_func):
    source_line = inspect.getsource(lambda_func)
    r = re.search(r'lambda:\s*(.+)\s*\)', source_line)
    return r.group(1)
