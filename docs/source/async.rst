Async support
=============

It's possible to us busypie in an async function,
and it's supported via 'until_async' function::

    from busypie import wait

    async def create_user():
        dispatch_user_create_command()
        await wait().until_async(lambda: user_created_dispatched)

Or with 'during_async' function::

    from busypie import wait

    async def create_user():
        dispatch_user_create_command()
        await wait().during_async(lambda: !app.has_user(user))

