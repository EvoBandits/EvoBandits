import gmab
import pytest
from pytest import LogCaptureFixture

from tests._functions.rosenbrock import rb_function


def test_best_trial(caplog: LogCaptureFixture):
    study = gmab.Study()

    # best_trial requires running study.optimize()
    with pytest.raises(RuntimeError):
        result = study.best_trial

    params = {"number": gmab.IntParam(-5, 10, size=2)}
    n_simulations = 10_000
    study.optimize(rb_function, params, n_simulations)
    assert "completed" in caplog.text  # integrates logging

    result = study.best_trial
    assert result == {"number": [1, 1]}
