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

from random import Random

import pytest
from evobandits import CategoricalParam, IntParam
from evobandits.study.study import Study


@pytest.mark.parametrize(
    "params, exp_bounds",
    [
        [{"a": IntParam(0, 1)}, [(0, 1)]],
        [{"a": IntParam(0, 1, 2)}, [(0, 1), (0, 1)]],
        [{"a": IntParam(0, 1, 2), "b": CategoricalParam([False, True])}, [(0, 1), (0, 1), (0, 1)]],
    ],
    ids=[
        "one_dimension",
        "one_param",
        "multiple_params",
    ],
)
def test_collect_bounds(params, exp_bounds):
    # Mock or patch dependencies
    study = Study(seed=42)  # with seed to avoid warning logs
    study._params = params

    # Collect bounds and verify result
    bounds = study._collect_bounds()
    assert bounds == exp_bounds


@pytest.mark.parametrize(
    "params, action_vector, exp_solution",
    [
        [{"a": IntParam(0, 1)}, [1], {"a": 1}],
        [{"a": IntParam(0, 1, 2)}, [0, 1, 0], {"a": [0, 1]}],
        [
            {"a": IntParam(0, 1, 2), "b": CategoricalParam([False, True])},
            [0, 1, 1],
            {"a": [0, 1], "b": True},
        ],
    ],
    ids=[
        "one_dimension",
        "one_param",
        "multiple_params",
    ],
)
def test_decode(params, action_vector, exp_solution):
    # Mock or patch dependencies
    study = Study(seed=42)  # with seed to avoid warning logs
    study._params = params

    # Decode an action vector and verify result
    solution = study._decode(action_vector)
    assert solution == exp_solution


@pytest.mark.parametrize(
    "params, action_vector, exp_result, kwargs",
    [
        [{"a": IntParam(0, 1, 2)}, [0, 1], -0.5, {}],
        [{"a": IntParam(0, 1, 2), "b": CategoricalParam([False, True])}, [0, 1, 1], 0.5, {}],
        [{"a": IntParam(0, 1, 2)}, [0, 1], +0.5, {"_direction": -1}],  # maximize objective
    ],
    ids=[
        "one_param",
        "multiple_params",
        "one_param_switch_direction",
    ],
)
def test_evaluate(params, action_vector, exp_result, kwargs):
    # Mock or patch dependencies
    def dummy_objective(a: list, b: bool = False):
        return sum(a) * 0.5 if b else -sum(a) * 0.5

    study = Study(seed=42)  # with seed to avoid warning logs
    study._params = params
    study._objective = dummy_objective
    study._direction = kwargs.get("_direction", 1)

    # Verify if study evaluates the objective
    result = study._evaluate(action_vector)
    assert result == exp_result


@pytest.mark.parametrize(
    "study, other_study, expected_eq",
    [
        [Study(), Study(), False],
        [Study(seed=42), Study(seed=42), True],
        [Study(seed=42), Study(), False],
    ],
    ids=["default", "seeded", "mixed"],
)
def test_study_seed_generator(study, other_study, expected_eq):
    # Verify generator
    assert isinstance(study.rng, Random)

    seed = study._generate_seed()
    assert isinstance(seed, int)

    # Verify seeded / unseeded behaviour
    seed_eq = seed == other_study._generate_seed()
    assert seed_eq == expected_eq
