from unittest.mock import MagicMock

import pytest
from gmab import Study, suggest_int

from tests._func import rosenbrock as rb


@pytest.mark.parametrize(
    "func, params, trials, exp_bounds",
    [
        pytest.param(rb.func, {"x": suggest_int(-5, 10, 2)}, 1, [(-5, 10), (-5, 10)], id="base"),
        pytest.param(rb.func, {"x": suggest_int(-5, 10, 2, 2)}, 1, [(-5, 3), (-5, 3)], id="step"),
        # ToDo: Test and Implement the input validaton for study.optimize
    ],
)
def test_optimize(func, params, trials, exp_bounds):
    # Dependency Injection to mock rust-gmab for testing.
    mock_algo = MagicMock()
    mock_algo.optimize.return_value = [1, 1]

    study = Study(algorithm=mock_algo)
    study.optimize(func, params, trials)
    mock_algo.assert_called_once_with(study._run_trial, exp_bounds)
    mock_algo.return_value.optimize.assert_called_once_with(trials)
