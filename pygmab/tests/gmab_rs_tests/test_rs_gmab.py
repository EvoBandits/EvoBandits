from contextlib import nullcontext

import pytest
from gmab import Gmab

from tests._functions import rosenbrock as rb

SEED = 42
POP = 10
MR = 0.1
CR = 0.9


@pytest.mark.parametrize(
    "bounds, budget, kwargs",
    [
        [[(0, 100), (0, 100)] * 5, 100, {}],
        [[(0, 100), (0, 100)] * 5, 100, {"seed": SEED}],
        [[(0, 100), (0, 100)] * 5, 100, {"population_size": POP}],
        [[(0, 100), (0, 100)] * 5, 100, {"mutation_rate": MR}],
        [[(0, 100), (0, 100)] * 5, 100, {"crossover_rate": CR}],
        [[(0, 10), (0, 10)], 100, {"population_size": 0, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"mutation_rate": -0.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"crossover_rate": 1.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 1), (0, 1)], None, {"exp": pytest.raises(RuntimeError)}],
    ],
    ids=[
        "success",
        "success_with_seed",
        "success_with_population_size",
        "success_with_mutation_rate",
        "success_with_crossover_rate",
        "fail_population_size_value",
        "fail_mutation_rate_value",
        "fail_crossover_rate_value",
        "fail_population_size_solution_size",
    ],
)
def test_gmab(bounds, budget, kwargs):
    expectation = kwargs.pop("exp", nullcontext())
    with expectation:
        gmab = Gmab(rb.function, bounds, **kwargs)
        _ = gmab.optimize(budget)
