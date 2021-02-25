Timeouts
========

The default timeout

To specify how much time will it will wait before it will fail on timeout::

    wait().at_most(FIVE_SECONDS).until(condition_function)
    # OR
    wait_at_most(FIVE_SECONDS).until(condition_function)
    # OR
    wait_at_most(5, SECOND).until(condition_function)

Upon a timeout it will raise the 'ConditionTimeoutError' exception, with the following message::

    Failed to meet condition of <description> within X seconds

For description there are 3 options:

- If the condition is a lambda, the description will be the content of the lambda
- If the condition is a function, the description will be the name of the function
- You can also define the description by using::

    wait().with_description('check app is running').until(lambda: app_state() == 'UP')

