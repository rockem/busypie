Assertion support
=================

Sometimes it's more convinient to way for an assert to pass instead
of checking a boolean expression. It's possible to achieve it with the
``until_asserted`` method. It will wait until no AssertionError exception will be thrown::

    from busypie import wait

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().until_asserted(validate_dispatched_event)

    def validate_dispatched_event():
        assert event.dispatched

``until_asserted`` support being called inside an async function as well::

    async def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        await wait().until_asserted_async(validate_dispatched_event)
