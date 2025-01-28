import pytest
from gmab.trial.trial import Trial


@pytest.fixture(autouse=True)
def reset_trial():
    Trial.reset()  # reset the singleton before each test.


def test_suggest_int():
    _trial = Trial()
    _trial.suggest_int("x", 0, 10)
    assert _trial.bounds == [(0, 10)]


def test_suggest_int_with_size():
    _trial = Trial()
    _trial.suggest_int("x", 0, 10, 3)
    assert _trial.bounds == [(0, 10), (0, 10), (0, 10)]
