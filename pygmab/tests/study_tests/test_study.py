from unittest.mock import MagicMock

import pytest
from gmab import Study, suggest_int

from tests._func import rosenbrock

xTypeErr = pytest.mark.xfail(raises=TypeError)
xValueErr = pytest.mark.xfail(raises=ValueError)

PARAMS = {"x": suggest_int(-5, 10, 2)}
EXP_BOUNDS = [(-5, 10), (-5, 10)]


@pytest.mark.parametrize(
    "func, params, trials, exp_bounds",
    [
        pytest.param(rosenbrock.func, PARAMS, 1, EXP_BOUNDS, id="base"),
        pytest.param("func", PARAMS, 1, EXP_BOUNDS, marks=xTypeErr, id="f_func_type"),
        pytest.param(rosenbrock.func, "PARAMS", 1, EXP_BOUNDS, marks=xTypeErr, id="f_params_type"),
        pytest.param(rosenbrock.func, PARAMS, 1.0, EXP_BOUNDS, marks=xTypeErr, id="f_trials_type"),
        pytest.param(rosenbrock.func, PARAMS, 0, EXP_BOUNDS, marks=xValueErr, id="f_trials_value"),
    ],
)
def test_optimize(func, params, trials, exp_bounds):
    # Dependency Injection to mock rust-gmab for testing.
    mock_algo = MagicMock()
    mock_algo.optimize.return_value = [1, 1]

    study = Study(algorithm=mock_algo)
    study.optimize(func, params, trials)
    mock_algo.assert_called_once_with(func, exp_bounds)
    mock_algo.return_value.optimize.assert_called_once_with(trials)
