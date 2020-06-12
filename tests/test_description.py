import pytest

from busypie import ConditionTimeoutError, ONE_HUNDRED_MILLISECONDS, wait_at_most


def test_custom_description_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).with_description('kuku').until(lambda: False)
    assert 'kuku' == e.value.description


def test_error_message_include_description():
    assert 'check desc' in ConditionTimeoutError('check desc', 0).args[0]


def test_condition_function_name_description_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).until(_always_fail_check)
    assert '_always_fail_check' == e.value.description


def test_lambda_content_description_on_timeout():
    with pytest.raises(ConditionTimeoutError) as e:
        wait_at_most(ONE_HUNDRED_MILLISECONDS).until(lambda: 3 == 4)
    assert '3 == 4' == e.value.description


def _always_fail_check():
    return False
