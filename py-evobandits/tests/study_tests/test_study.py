from contextlib import nullcontext
from unittest.mock import MagicMock

import pytest
from evobandits.study.study import ALGORITHM_DEFAULT, Study

from tests._functions import rosenbrock as rb


@pytest.mark.parametrize(
    "seed, kwargs, exp_algorithm",
    [
        [None, {"log": ("WARNING", "No seed provided")}, ALGORITHM_DEFAULT],
        [42, {}, ALGORITHM_DEFAULT],
        [42.0, {"exp": pytest.raises(TypeError)}, ALGORITHM_DEFAULT],
    ],
    ids=[
        "default",
        "default_with_seed",
        "fail_seed_type",
    ],
)
def test_study_init(seed, kwargs, exp_algorithm, caplog):
    # Extract expected exceptions and logs
    expectation = kwargs.pop("exp", nullcontext())
    log = kwargs.pop("log", None)

    # Initialize a Study and verify its properties
    with expectation:
        study = Study(seed, **kwargs)
        assert study.seed == seed
        assert study.algorithm == exp_algorithm
        assert study.objective is None
        assert study.params is None

        if log:
            level, msg = log
            matched = any(
                record.levelname == level and msg in record.message for record in caplog.records
            )
            assert matched, f"Expected {level} log containing '{msg}'"


@pytest.mark.parametrize(
    "objective, params, trials, best_trial, kwargs, mock_opt_result",
    [
        [rb.function, rb.PARAMS_2D, 1, rb.BEST_TRIAL_2D, {}, rb.RESULTS_2D],
    ],
    ids=[
        "valid_testcase_rosenbrock",
    ],
)
def test_optimize(objective, params, trials, best_trial, kwargs, mock_opt_result):
    # Mock dependencies
    mock_algorithm = MagicMock()
    mock_algorithm.optimize.return_value = mock_opt_result
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log

    # Extract expected exceptions
    expectation = kwargs.pop("exp", nullcontext())

    # Optimize a study and verify results
    with expectation:
        result = study.optimize(objective, params, trials)
        assert result == best_trial
        assert mock_algorithm.optimize.call_count == 1  # Always run algorithm once for now
