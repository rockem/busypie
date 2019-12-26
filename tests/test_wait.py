import pytest

from busypie import wait, wait_at_most, ConditionTimeoutError, \
    FIVE_HUNDRED_MILLISECONDS, MILLISECOND


@pytest.mark.timeout(1)
def test_timeout_when_condition_did_not_meet_in_time():
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(FIVE_HUNDRED_MILLISECONDS).until(lambda: 1 == 2)
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(100, MILLISECOND).until(lambda: False)
    with pytest.raises(ConditionTimeoutError):
        wait_at_most(100, MILLISECOND).until(lambda: 'Pizza' == 'Pie')
