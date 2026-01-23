Exception handling
==================

Sometimes it's useful to ignore exceptions that may be raised by the condition function::

    wait().ignore_exceptions().until(lambda: app.is_healthy())

You can also specify which exceptions to ignore::

    wait().ignore_exceptions(ZeroDivisionError, AttributeError).until(lambda: app.is_healthy())
