Assertion support
=================

Sometimes it's more convenient to wait for an assertion to pass rather than
checking a boolean expression. You can achieve this with the
``until_asserted`` method, which waits until no ``AssertionError`` is raised::

    from busypie import wait

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().until_asserted(validate_dispatched_event)

    def validate_dispatched_event():
        assert event.dispatched
        assert event.id == VALID_ID

``until_asserted`` also works inside async functions::

    async def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        await wait().until_asserted_async(validate_dispatched_event)
