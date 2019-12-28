from busypie import given, wait, ONE_SECOND, wait_at_most, MILLISECOND


def test_start_with_given():
    assert given() == wait()
    assert given().wait().at_most(ONE_SECOND) == wait().at_most(ONE_SECOND)


def test_combine_wait_and_at_most():
    assert wait().at_most(ONE_SECOND) == wait_at_most(ONE_SECOND)
    assert wait().at_most(2, MILLISECOND) == wait_at_most(2, MILLISECOND)
    assert given().wait_at_most(2, MILLISECOND) == wait().at_most(2, MILLISECOND)


