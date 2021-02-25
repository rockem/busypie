Quickstart
==========

Most typical usage will be in test, when we have a scenario
that require us to wait for something to happen::

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().until(event_dispatched)

We can also wait while a condition exists::

    def test_event_should_be_dispatched():
        dispatcher.dispatch(event)
        wait().during(event_not_dispatched)
