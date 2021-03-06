Quickstart
==========

Most typical usage will be in test, when we have a scenario
that require us to wait for something to happen::

    from busypie import wait

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().until(event_dispatched)

It's also possible to wait while something happens::

    from busypie import wait, MINUTE

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().at_most(2 * MINUTE).during(event_not_dispatched)
