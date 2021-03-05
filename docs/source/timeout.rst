Timeout
=======

Timeout error
-------------
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
