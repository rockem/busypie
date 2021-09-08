import pytest

from busypie import set_default_timeout, wait, reset_defaults, MILLISECOND, ConditionTimeoutError
from tests.sleeper import assert_done_after


@pytest.mark.timeout(0.6)
def test_set_default_timeout():
    set_default_timeout(500, MILLISECOND)
    with pytest.raises(ConditionTimeoutError):
        wait().until(lambda: 1 == 2)


def test_reset_default_timeout():
    set_default_timeout(200, MILLISECOND)
    reset_defaults()
    with assert_done_after(seconds=0.4) as c:
        wait().until(lambda: c.done)
