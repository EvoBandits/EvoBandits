from gmab.trial.trial import trial


def test_suggest_int():
    trial.suggest_int("x", 0, 10, 2)
    assert trial.bounds == [(0, 10), (0, 10)]
