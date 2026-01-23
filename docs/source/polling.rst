Polling
=======

Poll interval
-------------
You can customize the time between each condition check.
This is called the polling interval::

    wait().poll_interval(1, SECOND).until(condition_function)


Poll delay
----------
Sometimes it's useful to delay the start of polling.
Specifying a poll delay will wait before the first condition check::

    wait().at_most(5 * MINUTE).poll_delay(ONE_MINUTE).until(user_created_dispatched)

**Note:** The timeout countdown starts immediately, regardless of the poll delay.
