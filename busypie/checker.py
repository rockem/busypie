from busypie.func import is_async


async def check(f):
    if is_async(f):
        return await f()
    return f()


async def negative_check(f):
    if is_async(f):
        result = await f()
        return not result
    return not f()


async def assert_check(f):
    if is_async(f):
        await f()
    else:
        f()
    return True
