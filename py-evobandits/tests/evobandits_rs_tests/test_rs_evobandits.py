from contextlib import nullcontext

import pytest
from evobandits import Arm, EvoBandits

from tests._functions import rosenbrock as rb


def test_arm():
    mock_av = [1, 1, 1]
    exp_dict = {"action_vector": mock_av, "mean_reward": 0.0, "num_pulls": 0}

    arm = Arm(mock_av)
    assert arm.action_vector == mock_av
    assert arm.num_pulls == 0
    assert arm.mean_reward == 0.0
    assert arm.to_dict == exp_dict


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"population_size": 10},
        {"mutation_rate": 0.1},
        {"crossover_rate": 0.9},
        {"mutation_span": 1.0},
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
        [[(0, 100), (0, 100)] * 5, 100, {"seed": 42}],
        [[(0, 100), (0, 100)] * 5, 100, {"top_k": 2}],
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
        "fail_population_size_value",  # ToDo Issue #57: Err should be raised in the constructor
        "fail_mutation_rate_value",  # ToDo Issue #57: Err should be raised in the constructor
        "fail_crossover_rate_value",  # ToDo Issue #57: Err should be raised in the constructor
        "fail_mutation_span_value",  # ToDo Issue #57: Err should be raised in the constructor
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

        assert all([isinstance(r, Arm) for r in result])
        assert len(result) == top_k
