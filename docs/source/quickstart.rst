Quickstart
==========

The most typical usage is in tests, when you have a scenario
that requires waiting for something to happen::

    from busypie import wait

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().until(event_dispatched)

Using it inside an async function is almost the same::

    from busypie import wait

    async def create_user():
        dispatch_user_create_command()
        await wait().until_async(lambda: user_created_dispatched)

You can also wait while a condition remains true::

    from busypie import wait, MINUTE

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().at_most(2 * MINUTE).during(event_not_dispatched)

As with ``until``, async support is available for ``during`` as well::

    from busypie import wait

    async def create_user():
        dispatch_user_create_command()
        await wait().during_async(lambda: not app.has_user(user))
