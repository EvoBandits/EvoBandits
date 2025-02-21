import gmab
import pytest
from pytest import LogCaptureFixture

from tests._func import rosenbrock


def test_best_trial(caplog: LogCaptureFixture):
    study = gmab.create_study()

    # best_trial requires running study.optimize()
    with pytest.raises(RuntimeError):
        result = study.best_trial

    params = {"number": gmab.suggest_int(-5, 10, size=2)}
    # bounds = [(-5, 10), (-5, 10)]
    n_simulations = 10_000
    study.optimize(rosenbrock.func, params, n_simulations)
    assert "completed" in caplog.text  # integrates logging

    result = study.best_trial
    assert result == [1, 1]  # returns expected result
