from busypie.func import is_async
from busypie.types import ConditionCallback


async def check(f: ConditionCallback) -> any:
    if is_async(f):
        return await f()
    return f()


async def negative_check(f: ConditionCallback) -> bool:
    if is_async(f):
        result = await f()
        return not result
    return not f()


async def assert_check(f: ConditionCallback) -> bool:
    if is_async(f):
        await f()
    else:
        f()
    return True
