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
from evobandits.params.int_param import IntParam

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
            {"n_best": 2, "optimize_ret": cl.ARMS_EXAMPLE, "_results_expected": cl.TRIALS_EXAMPLE},
        ],
        [rb.function, rb.PARAMS, 1, {"maximize": True}],
        [
            rb.function,
            rb.PARAMS,
            1,
            {
                "n_runs": 2,
                "_results_expected": [
                    {
                        "value": 0.0,
                        "value_std_dev": 0.0,
                        "n_evaluations": 0,
                        "params": {"number": [1, 1]},
                    },
                    {
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
        [rb.function, {"seed": IntParam(0, 100)}, 1, {"exp": pytest.raises(ValueError)}],
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
        "invalid_params_contains_seed",
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
    _results = kwargs.pop("_results_expected", rb.TRIAL_BEST)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log

    # Extract expected exceptions
    expectation = kwargs.pop("exp", nullcontext())

    # Optimize a study and verify results
    with expectation:
        study.optimize(objective, params, n_trials, **kwargs)

        assert study._results == _results
        assert mock_algorithm.optimize.call_count == kwargs.get("n_runs", 1)


@pytest.mark.parametrize(
    "raw_results, direction, expected_results",
    [
        (
            [
                {"id": 0, "value": 2.0, "n_evaluations": 1},
                {"id": 1, "value": 3.0, "n_evaluations": 1},
                {"id": 2, "value": 1.0, "n_evaluations": 1},
                {"id": 3, "value": 1.0, "n_evaluations": 2},
            ],
            1,
            [
                {"id": 3, "value": 1.0, "n_evaluations": 2, "ucb_rank": 1},
                {"id": 2, "value": 1.0, "n_evaluations": 1, "ucb_rank": 2},
                {"id": 0, "value": 2.0, "n_evaluations": 1, "ucb_rank": 3},
                {"id": 1, "value": 3.0, "n_evaluations": 1, "ucb_rank": 4},
            ],
        ),
        (
            [
                {"id": 0, "value": 2.0, "n_evaluations": 1},
                {"id": 1, "value": 3.0, "n_evaluations": 1},
                {"id": 2, "value": 1.0, "n_evaluations": 1},
                {"id": 3, "value": 3.0, "n_evaluations": 2},
            ],
            -1,
            [
                {"id": 3, "value": 3.0, "n_evaluations": 2, "ucb_rank": 1},
                {"id": 1, "value": 3.0, "n_evaluations": 1, "ucb_rank": 2},
                {"id": 0, "value": 2.0, "n_evaluations": 1, "ucb_rank": 3},
                {"id": 2, "value": 1.0, "n_evaluations": 1, "ucb_rank": 4},
            ],
        ),
        (
            [
                {"id": 0, "value": 1.0, "n_evaluations": 1},
                {"id": 1, "value": 1.0, "n_evaluations": 1},
                {"id": 2, "value": 1.0, "n_evaluations": 1},
            ],
            1,
            [
                {"id": 0, "value": 1.0, "n_evaluations": 1, "ucb_rank": 1},
                {"id": 1, "value": 1.0, "n_evaluations": 1, "ucb_rank": 2},
                {"id": 2, "value": 1.0, "n_evaluations": 1, "ucb_rank": 3},
            ],
        ),
    ],
    ids=["minimization", "maximization", "all_equal_means_rank_sequential"],
)
def test_results_property(raw_results, direction, expected_results):
    # Mock dependencies
    mock_algorithm = create_autospec(GMAB, instance=True)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log
    study._direction = direction
    study._results = raw_results

    assert study.results == expected_results


def test_results_property_raises_no_results():
    # Mock dependencies
    mock_algorithm = create_autospec(GMAB, instance=True)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log

    with pytest.raises(AttributeError):
        _ = study.results


@pytest.mark.parametrize(
    "direction, results, best_solution, best_params, best_value, mean_value",
    [
        [
            +1,
            [
                {
                    "value": 1.0,
                    "n_evaluations": 10,
                    "ucb_rank": 1,
                    "params": {"number": [1, 1]},
                },
                {
                    "value": 2.0,
                    "n_evaluations": 10,
                    "ucb_rank": 2,
                    "params": {"number": [2, 2]},
                },
                {
                    "value": 3.0,
                    "n_evaluations": 10,
                    "ucb_rank": 3,
                    "params": {"number": [3, 3]},
                },
            ],
            {
                "value": 1.0,
                "n_evaluations": 10,
                "ucb_rank": 1,
                "params": {"number": [1, 1]},
            },
            {"number": [1, 1]},
            1.0,
            2.0,
        ],
        [
            -1,
            [
                {
                    "value": 1.0,
                    "n_evaluations": 10,
                    "ucb_rank": 3,
                    "params": {"number": [1, 1]},
                },
                {
                    "value": 2.0,
                    "n_evaluations": 10,
                    "ucb_rank": 2,
                    "params": {"number": [2, 2]},
                },
                {
                    "value": 3.0,
                    "n_evaluations": 10,
                    "ucb_rank": 1,
                    "params": {"number": [3, 3]},
                },
            ],
            {
                "value": 3.0,
                "n_evaluations": 10,
                "ucb_rank": 1,
                "params": {"number": [3, 3]},
            },
            {"number": [3, 3]},
            3.0,
            2.0,
        ],
    ],
    ids=["default_minimize", "default_maximize"],
)
def test_output_properties(direction, results, best_solution, best_params, best_value, mean_value):
    # Mock dependencies
    mock_algorithm = create_autospec(GMAB, instance=True)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log
    study._direction = direction
    study._results = results

    # Access properties and verify
    assert study.best_solution == best_solution
    assert study.best_params == best_params
    assert study.best_value == best_value
    assert study.mean_value == mean_value


@pytest.mark.parametrize(
    "seed, objective, params, exp_value, expectation",
    [
        [None, rb.function, rb.PARAMS, False, nullcontext()],
        [42, rb.function, rb.PARAMS, False, nullcontext()],
        [None, rb.noisy_rosenbrock, rb.PARAMS, False, nullcontext()],
        [42, rb.noisy_rosenbrock, rb.PARAMS, True, nullcontext()],
    ],
    ids=[
        "no_seed_unseeded_func",
        "with_seed_unseeded_func",
        "no_seed_seeded_func",
        "with_seed_seeded_func",
    ],
)
def test_seeded_call_property(seed, objective, params, exp_value, expectation):
    study = Study(seed)
    study._objective = objective
    study._params = params

    with expectation:
        assert study.seeded_call == exp_value
