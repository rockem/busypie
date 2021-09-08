from functools import partial

import pytest

from busypie import ConditionTimeoutError, wait, ONE_HUNDRED_MILLISECONDS
from tests.sleeper import assert_done_after


def test_timeout_when_not_asserted_in_time():
    with pytest.raises(ConditionTimeoutError):
        wait().at_most(ONE_HUNDRED_MILLISECONDS).until_asserted(failed_assertion)


def test_wait_for_assertion_to_pass():
    with assert_done_after(seconds=0.3) as c:
        wait().until_asserted(partial(assert_is_done, c))


def failed_assertion():
    assert 1 == 2


def assert_is_done(sleeper):
    assert sleeper.done
