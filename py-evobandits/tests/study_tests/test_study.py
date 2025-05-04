from contextlib import nullcontext
from unittest.mock import MagicMock

import pytest
from evobandits import ALGORITHM_DEFAULT, EvoBandits, Study

from tests._functions import clustering as cl
from tests._functions import rosenbrock as rb


def test_algorithm_default():
    # the default algorithm should always be a new Evobandits instance without modifications
    assert ALGORITHM_DEFAULT == EvoBandits()


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
    "objective, params, trials, kwargs",
    [
        [rb.function, rb.PARAMS_2D, 1, {}],
        [
            cl.function,
            cl.PARAMS,
            1,
            {"mock_opt_return": cl.RESULTS_EXAMPLE, "mock_best_trial": cl.BEST_TRIAL_EXAMPLE},
        ],
    ],
    ids=[
        "valid_default_testcase",
        "valid_clustering_testcase",
    ],
)
def test_optimize(objective, params, trials, kwargs):
    # Mock dependencies
    # Per default, and expected results from the rosenbrock testcase are used to mock EvoBandits.
    mock_algorithm = MagicMock()
    mock_algorithm.optimize.return_value = kwargs.get("mock_opt_return", rb.RESULTS_2D)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log

    # Extract expected exceptions
    expectation = kwargs.pop("exp", nullcontext())

    # Optimize a study and verify results
    with expectation:
        best_trial = study.optimize(objective, params, trials)
        assert best_trial == kwargs.get("mock_best_trial", rb.BEST_TRIAL_2D)
        assert mock_algorithm.optimize.call_count == 1  # Always run algorithm once for now
