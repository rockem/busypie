Timeout
=======

You can specify the timeout using either ``wait`` or ``wait_at_most``::

    from busypie import wait, wait_at_most, SECOND

    wait().at_most(5 * SECOND).until(condition_function)
    wait_at_most(5 * SECOND).until(condition_function)

Condition timeout description
-----------------------------
When a timeout occurs, :pypi:`busypie` raises a ``ConditionTimeoutError`` exception with a message like::

    Failed to meet condition of <description> within X seconds

The description is determined as follows:

- If the condition is a lambda, the description is the lambda's source code
- If the condition is a function, the description is the function's name
- You can also provide a custom description::

    wait().with_description('check app is running').until(lambda: app_state() == 'UP')


Condition timeout cause
-----------------------
If an ignored exception was raised before the timeout, the
``ConditionTimeoutError`` will include that exception as its cause.

Return on timeout
-----------------
If needed, you can return ``False`` on timeout instead of raising a
``ConditionTimeoutError``::

    result = wait().return_on_timeout().until(lambda: app_state() == 'UP')
    if not result:
        handle_error()

Minimum wait time
-----------------
Sometimes you want to ensure that a condition is not met too quickly.
Use ``at_least`` to specify a minimum wait time::

    wait().at_least(2 * SECOND).until(condition_function)

If the condition is met before the minimum wait time, a ``ConditionTimeoutError``
will be raised. This is useful when you want to verify that a process takes
at least a certain amount of time.

You can combine ``at_least`` with ``at_most``::

    wait().at_least(2 * SECOND).at_most(10 * SECOND).until(condition_function)

Default timeout
---------------
The default timeout in :pypi:`busypie` is 10 seconds. You can change it using::

    from busypie import set_default_timeout

    set_default_timeout(1 * MINUTE)
