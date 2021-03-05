Timeout
=======

It's possible to specify the timeout either by wait or wait_at_most::

    from busypie import wait, wait_at_most, SECOND

    wait().at_most(5 * SECOND).until(condition_function)
    wait_at_most(5 * SECOND).until(condition_function)

Timeout description
-------------------
Upon a timeout busypie will raise a 'ConditionTimeoutError' exception, with the following message::

    Failed to meet condition of <description> within X seconds

For description there are 3 options:

- If the condition is a lambda, the description will be the content of the lambda
- If the condition is a function, the description will be the name of the function
- You can also define the description by using::

    wait().with_description('check app is running').until(lambda: app_state() == 'UP')

Default timeout
---------------
While the default timeout in busypie is set to 10 seconds, you can change using::

    from busypie import set_default_timeout

    set_default_timeout(1 * MINUTE)
