
def wait():
    return ConditionBuilder()


class ConditionBuilder:

    def until(self, func):
        pass


class ConditionTimeoutError(Exception):
    pass
