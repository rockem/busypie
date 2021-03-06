Durations
=========

Every function in :pypi:`busypie` that accepts duration, support both number of seconds
and time/unit input. For specifying duration with number of seconds do::

    wait().at_most(5).until(lambda: app.is_healthy())
    wait().at_most(2 * MINUTE).until(lambda: app.is_healthy())

Or specify the unit of measurement::

    wait().at_most(5, SECONDS).until(lambda: app.is_healthy())
    wait().at_most(2, MINUTE).until(lambda: app.is_healthy())

Predefined durations
--------------------
:pypi:`busypie` supports these duration constants out of the box

- MILLISECOND
- SECOND
- MINUTE
- HOUR
- ONE_HUNDRED_MILLISECONDS
- FIVE_HUNDRED_MILLISECONDS
- ONE_SECOND
- TWO_SECONDS
- FIVE_SECONDS
- TEN_SECONDS
- ONE_MINUTE
- TWO_MINUTES
- FIVE_MINUTES
- TEN_MINUTES
