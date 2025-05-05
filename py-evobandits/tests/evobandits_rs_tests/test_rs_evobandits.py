from contextlib import nullcontext

import pytest
from evobandits import EvoBandits

from tests._functions import rosenbrock as rb

SEED = 42
POPULATION_SIZE = 10
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.9
MUTATION_SPAN = 1.0
TOP_K = 2


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"population_size": POPULATION_SIZE},
        {"mutation_rate": MUTATION_RATE},
        {"crossover_rate": CROSSOVER_RATE},
        {"mutation_span": MUTATION_SPAN},
    ],
    ids=[
        "default",
        "with_population_size",
        "with_mutation_rate",
        "with_crossover_rate",
        "with_mutation_span",
    ],
)
def test_evobandits_init(kwargs):
    expectation = kwargs.pop("exp", nullcontext())
    with expectation:
        evobandits = EvoBandits(**kwargs)
        assert isinstance(evobandits, EvoBandits)


@pytest.mark.parametrize(
    "bounds, budget, kwargs",
    [
        [[(0, 100), (0, 100)] * 5, 100, {}],
        [[(0, 100), (0, 100)] * 5, 100, {"seed": SEED}],
        [[(0, 100), (0, 100)] * 5, 100, {"top_k": TOP_K}],
        [[(0, 100), (0, 100)] * 5, 1, {"population_size": 2, "exp": pytest.raises(RuntimeError)}],
        [[(0, 100), (0, 100)] * 5, 1, {"top_k": 0, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"population_size": 0, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"mutation_rate": -0.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"crossover_rate": 1.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 10), (0, 10)], 100, {"mutation_span": -0.1, "exp": pytest.raises(RuntimeError)}],
        [[(0, 1), (0, 1)], 100, {"exp": pytest.raises(RuntimeError)}],
    ],
    ids=[
        "success",
        "success_with_seed",
        "success_with_top_k",
        "fail_budget_value",
        "fail_top_k_value",
        "fail_population_size_value",  # ToDo Issue #57: Errors should be raised in the constructor
        "fail_mutation_rate_value",  # ToDo Issue #57: Errors should be raised in the constructor
        "fail_crossover_rate_value",  # ToDo Issue #57: Errors should be raised in the constructor
        "fail_mutation_span_value",  # ToDo Issue #57: Errors should be raised in the constructor
        "fail_population_size_solution_size",
    ],
)
def test_evobandits(bounds, budget, kwargs):
    expectation = kwargs.pop("exp", nullcontext())
    seed = kwargs.pop("seed", None)
    top_k = kwargs.pop("top_k", 1)
    with expectation:
        evobandits = EvoBandits(**kwargs)
        result = evobandits.optimize(rb.function, bounds, budget, top_k, seed)

        # Check if results dict is valid:
        # Contains top_k action_vectors, mean_results, num_evaluations, and nothing else
        assert isinstance(result, dict)

        expected = {"action_vector", "mean_result", "num_evaluations", "top_k"}
        assert set(result.keys()) == expected

        for v in result.values():
            assert isinstance(v, list)
            assert len(v) == top_k
