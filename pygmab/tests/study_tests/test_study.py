from unittest.mock import MagicMock

import pytest
from gmab import Study, suggest_int

from tests._func import rosenbrock

EXP_BOUNDS = [(-5, 10), (-5, 10)]


@pytest.mark.parametrize(
    "func, params, trials, exp_bounds",
    [
        pytest.param(rosenbrock.func, {"x": suggest_int(-5, 10, 2)}, 1, EXP_BOUNDS, id="base"),
        pytest.param(rosenbrock.func, {"x": suggest_int(-5, 10, 2, 2)}, 1, EXP_BOUNDS, id="base"),
        # ToDo: Test and Implement the input for study.optimize
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
