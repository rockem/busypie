Polling
=======

Polling Interval
----------------
It's possible to alter the time that pass between each condition function call.
This interval is called the polling interval::

    wait().poll_interval(1, SECOND).until(condition_function)


Polling Delay
-------------
Sometimes it's helpful to delay the polling for a specific time.
Specifying the poll delay will delay the start of the polling.
NOTE: the timout count will start immediately regardless of the poll delay::

    wait().at_most(5 * MINUTE).poll_delay(ONE_MINUTE).until(user_created_dispatched)

