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

import pytest
from evobandits import EvoBandits

from tests._functions import rosenbrock as rb

SEED = 42
POPULATION_SIZE = 10
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.9
MUTATION_SPAN = 1.0


@pytest.mark.parametrize(
    "bounds, budget, kwargs",
    [
        [[(0, 100), (0, 100)] * 5, 100, {}],
        [[(0, 100), (0, 100)] * 5, 100, {"seed": SEED}],
        [[(0, 100), (0, 100)] * 5, 100, {"population_size": POPULATION_SIZE}],
        [[(0, 100), (0, 100)] * 5, 100, {"mutation_rate": MUTATION_RATE}],
        [[(0, 100), (0, 100)] * 5, 100, {"crossover_rate": CROSSOVER_RATE}],
        [[(0, 100), (0, 100)] * 5, 100, {"mutation_span": MUTATION_SPAN}],
        [[(0, 100), (0, 100)] * 5, 1, {"population_size": 2, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"population_size": 0, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"mutation_rate": -0.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"crossover_rate": 1.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"mutation_span": -0.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 1), (0, 1)], 100, {"exp": pytest.raises(RuntimeError)}],
    ],
    ids=[
        "success",
        "success_with_seed",
        "success_with_population_size",
        "success_with_mutation_rate",
        "success_with_crossover_rate",
        "success_with_mutation_span",
        "fail_budget_value",
        "fail_population_size_value",
        "fail_mutation_rate_value",
        "fail_crossover_rate_value",
        "fail_mutation_span_value",
        "fail_population_size_solution_size",
    ],
)
def test_evobandits(bounds, budget, kwargs):
    expectation = kwargs.pop("exp", nullcontext())
    seed = kwargs.pop("seed", None)
    with expectation:
        evobandits = EvoBandits(**kwargs)
        _ = evobandits.optimize(rb.function, bounds, budget, seed)


@pytest.mark.parametrize(
    "this, other, expected_eq",
    [
        [EvoBandits(), EvoBandits(), True],
        [EvoBandits(population_size=1), EvoBandits(population_size=1), True],
        [EvoBandits(), EvoBandits(population_size=1), False],
    ],
    ids=["default_eq", "modified_eq", "not_eq"],
)
def test_evobandits_eq(this, other, expected_eq):
    assert (this == other) == expected_eq
