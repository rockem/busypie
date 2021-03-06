Polling
=======

Poll interval
----------------
It's possible to alter the time that passes between each condition function call.
This interval is called the polling interval::

    wait().poll_interval(1, SECOND).until(condition_function)


Poll delay
-------------
Sometimes it's useful to delay the polling for a specific time.
Specifying the poll delay will delay the start of the polling::

    wait().at_most(5 * MINUTE).poll_delay(ONE_MINUTE).until(user_created_dispatched)

NOTE: the timeout count will start immediately regardless of the poll delay