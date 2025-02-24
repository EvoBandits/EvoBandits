from unittest.mock import MagicMock

import pytest
from gmab import IntParam, Study

from tests._func import rosenbrock as rb


@pytest.mark.parametrize(
    "func, params, trials, exp_bounds",
    [
        pytest.param(rb.func, {"x": IntParam(-5, 10, 2)}, 1, [(-5, 10), (-5, 10)], id="base"),
        pytest.param(rb.func, {"x": IntParam(-5, 10, 2, 2)}, 1, [(-5, 3), (-5, 3)], id="step"),
        # ToDo: Implement the input validaton for study.optimize
    ],
)
def test_optimize(func, params, trials, exp_bounds):
    mock_gmab = MagicMock()
    mock_gmab.optimize.return_value = [1, 1]

    study = Study(algorithm=mock_gmab)
    study.optimize(func, params, trials)

    mock_gmab.assert_called_once_with(study._run_trial, exp_bounds)  # Use of Gmab(...)
    mock_gmab.return_value.optimize.assert_called_once_with(trials)  # Use of gmab.optimize(...)
