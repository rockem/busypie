Assertion support
=================

Sometimes it's more convenient to wait for an assertion to pass instead
of checking a boolean expression. It's possible to achieve this with the
``until_asserted`` method. It will wait until no AssertionError exception will be thrown::

    from busypie import wait

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().until_asserted(validate_dispatched_event)

    def validate_dispatched_event():
        assert event.dispatched
        assert event.id == VALID_ID

``until_asserted`` supports being called inside an async function as well::

    async def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        await wait().until_asserted_async(validate_dispatched_event)

