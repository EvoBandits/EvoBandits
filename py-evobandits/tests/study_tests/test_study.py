from contextlib import nullcontext
from unittest.mock import MagicMock

import pytest
from evobandits.study.study import ALGORITHM_DEFAULT, Study

from tests._functions import clustering as cl
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
    "func, params, trials",
    [
        [rb.function, rb.PARAMS_2D, 1],
        [cl.function, cl.PARAMS, 1],
    ],
    ids=[
        "try_rosenbrock",  # Simple case with one integer parameter
        "try_clustering",  # Case with multiple parameters and various types
        # ToDo: Input validation: Fail if func is not callable
        # ToDo: Input validation: Fail if params is not valid
        # ToDo: Input validation: Fail if trials is not positive integer
    ],
)
def test_study_optimize(func, params, trials):
    mock = MagicMock()  # Mock EvoBandits Algorithm
    study = Study(algorithm=mock)
    study.optimize(func, params, trials)
    assert mock.optimize.call_count == 1  # Ensure EvoBandits was called exactly once
