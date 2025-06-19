# Copyright 2025 EvoBandits
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from contextlib import nullcontext
from unittest.mock import create_autospec

import pytest
from evobandits import ALGORITHM_DEFAULT, GMAB, Study

from tests._functions import clustering as cl
from tests._functions import rosenbrock as rb


def test_algorithm_default():
    # the default algorithm should always be a new GMAB instance without modifications
    assert ALGORITHM_DEFAULT == GMAB()


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

        if log:
            level, msg = log
            matched = any(
                record.levelname == level and msg in record.message for record in caplog.records
            )
            assert matched, f"Expected {level} log containing '{msg}'"


@pytest.mark.parametrize(
    "objective, params, n_trials, kwargs",
    [
        [rb.function, rb.PARAMS, 1, {}],
        [
            cl.function,
            cl.PARAMS,
            2,
            {"n_best": 2, "optimize_ret": cl.ARMS_EXAMPLE, "exp_result": cl.TRIALS_EXAMPLE},
        ],
        [rb.function, rb.PARAMS, 1, {"maximize": True}],
        [
            rb.function,
            rb.PARAMS,
            1,
            {
                "n_runs": 2,
                "exp_result": [
                    {
                        "run_id": 0,
                        "n_best": 1,
                        "value": 0.0,
                        "value_std_dev": 0.0,
                        "n_evaluations": 0,
                        "params": {"number": [1, 1]},
                    },
                    {
                        "run_id": 1,
                        "n_best": 1,
                        "value": 0.0,
                        "value_std_dev": 0.0,
                        "n_evaluations": 0,
                        "params": {"number": [1, 1]},
                    },
                ],
            },
        ],
        [rb.function, ["number"], 1, {"exp": pytest.raises(TypeError)}],
        [rb.function, {1: "number"}, 1, {"exp": pytest.raises(TypeError)}],
        [rb.function, {"number": "BaseParam"}, 1, {"exp": pytest.raises(TypeError)}],
        [rb.function, rb.PARAMS, 1, {"maximize": "False", "exp": pytest.raises(TypeError)}],
        [rb.function, rb.PARAMS, 1, {"n_runs": "2", "exp": pytest.raises(TypeError)}],
        [rb.function, rb.PARAMS, 1, {"n_runs": 0, "exp": pytest.raises(ValueError)}],
    ],
    ids=[
        "valid_default_testcase",
        "valid_clustering_testcase",
        "default_with_maximize",
        "default_with_n_runs",
        "invalid_params_not_a_mapping",
        "invalid_params_not_a_str_key",
        "invalid_params_not_a_BaseParam_value",
        "invalid_maximize_type",
        "invalid_n_runs_type",
        "invalid_n_runs_value",
    ],
)
def test_optimize(objective, params, n_trials, kwargs):
    # Mock dependencies
    mock_algorithm = create_autospec(GMAB, instance=True)
    mock_algorithm.optimize.return_value = kwargs.pop("optimize_ret", rb.ARM_BEST)
    mock_algorithm.clone.return_value = mock_algorithm
    exp_result = kwargs.pop("exp_result", rb.TRIAL_BEST)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log

    # Extract expected exceptions
    expectation = kwargs.pop("exp", nullcontext())

    # Optimize a study and verify results
    with expectation:
        study.optimize(objective, params, n_trials, **kwargs)

        result = study.results
        assert result == exp_result
        assert mock_algorithm.optimize.call_count == kwargs.get("n_runs", 1)


@pytest.mark.parametrize(
    "direction, best_solution, best_params, best_value, mean_value",
    [
        [
            +1,
            {
                "value": 1.0,
                "num_pulls": 10,
                "params": {"number": [1, 1]},
            },
            {"number": [1, 1]},
            1.0,
            2.0,
        ],
        [
            -1,
            {
                "value": 3.0,
                "num_pulls": 10,
                "params": {"number": [3, 3]},
            },
            {"number": [3, 3]},
            3.0,
            2.0,
        ],
    ],
    ids=["default_minimize", "default_maximize"],
)
def test_study_properties(direction, best_solution, best_params, best_value, mean_value):
    # Mock dependencies
    mock_algorithm = create_autospec(GMAB, instance=True)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log
    study._direction = direction
    study.results = [
        {
            "value": 1.0,
            "num_pulls": 10,
            "params": {"number": [1, 1]},
        },
        {
            "value": 2.0,
            "num_pulls": 10,
            "params": {"number": [2, 2]},
        },
        {
            "value": 3.0,
            "num_pulls": 10,
            "params": {"number": [3, 3]},
        },
    ]

    # Access properties and verify
    assert study.best_solution == best_solution
    assert study.best_params == best_params
    assert study.best_value == best_value
    assert study.mean_value == mean_value
