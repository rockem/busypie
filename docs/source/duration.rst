Durations
=========

Every function in :pypi:`busypie` that accepts a duration supports both a plain number of seconds
and a time/unit format. To specify a duration in seconds::

    wait().at_most(5).until(lambda: app.is_healthy())
    wait().at_most(2 * MINUTE).until(lambda: app.is_healthy())

Or specify the unit of measurement explicitly::

    wait().at_most(5, SECONDS).until(lambda: app.is_healthy())
    wait().at_most(2, MINUTE).until(lambda: app.is_healthy())

Predefined durations
--------------------
:pypi:`busypie` provides these duration constants out of the box:

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
