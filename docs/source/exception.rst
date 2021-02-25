Exceptions handling
===================

Sometimes you'll want to wait while ignoring any exception
that might be thrown::

    wait().ignore_exceptions().until(lambda: app.is_healthy())

It's also possible to ignore specific exceptions::

    wait().ignore_exceptions(ZeroDevisionError, AttributeError).until(lambda: app.is_healthy())

