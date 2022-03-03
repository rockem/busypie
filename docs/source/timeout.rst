Timeout
=======

It's possible to specify the timeout either by wait or wait_at_most::

    from busypie import wait, wait_at_most, SECOND

    wait().at_most(5 * SECOND).until(condition_function)
    wait_at_most(5 * SECOND).until(condition_function)

Condition timeout description
-----------------------------
Upon a timeout :pypi:`busypie` will raise a 'ConditionTimeoutError' exception, with the following message::

    Failed to meet condition of <description> within X seconds

For description there are 3 options:

- If the condition is a lambda, the description will be the content of the lambda
- If the condition is a function, the description will be the name of the function
- It's also possible to define the description by using::

    wait().with_description('check app is running').until(lambda: app_state() == 'UP')


Condition timeout cause
-----------------------
If there was an ignored exception that was thrown prior to the the timeout, the
'ConditionTimeoutError' error, will contain that last exception as the cause for it.

Default timeout
---------------
The default timeout in :pypi:`busypie` is set to 10 seconds, you can change that by using::

    from busypie import set_default_timeout

    set_default_timeout(1 * MINUTE)

