from functools import partial

import pytest

from busypie import ONE_HUNDRED_MILLISECONDS, ConditionTimeoutError, wait_at_most


def test_custom_description_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).with_description("kuku").until(
            lambda: False
        )
    assert "kuku" == e.value.description


def test_error_message_include_description():
    assert "check desc" in ConditionTimeoutError("check desc", 0).args[0]


def test_condition_function_name_description_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).until(_always_fail_check)
    assert "_always_fail_check" == e.value.description


def test_partial_condition_function_name_description_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).until(partial(_always_fail_check, x=42))
    assert "_always_fail_check" == e.value.description


def test_lambda_content_description_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).until(lambda: 3 == 4)
    assert "3 == 4" == e.value.description


def test_lambda_content_with_captures():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).until(lambda x=1, y=2: x == y)
    assert "x == y" == e.value.description


def _always_fail_check(x=10):
    return x == 0
