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
    study.params = params

    # Collect bounds and verify result
    bounds = study._collect_bounds()
    assert bounds == exp_bounds


@pytest.mark.parametrize(
    "params, action_vector, exp_solution",
    [
        [{"a": IntParam(0, 1)}, [1], {"a": 1}],
        [{"a": IntParam(0, 1, 3)}, [0, 1, 0], {"a": [0, 1, 0]}],
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
    study.params = params

    # Decode an action vector and verify result
    solution = study._decode(action_vector)
    assert solution == exp_solution


@pytest.mark.parametrize(
    "params, action_vector, exp_solution",
    [
        [{"a": IntParam(0, 1, 3)}, [0, 1, 0], {"a": [0, 1, 0]}],
        [
            {"a": IntParam(0, 1, 2), "b": CategoricalParam([False, True])},
            [0, 1, 1],
            {"a": [0, 1], "b": True},
        ],
    ],
    ids=[
        "one_param",
        "multiple_params",
    ],
)
def test_evaluate(params, action_vector, exp_solution):
    # Mock or patch dependencies
    def dummy_objective(a: list, b: bool = False):
        return sum(a) if b else -sum(a)

    study = Study(seed=42)  # with seed to avoid warning logs
    study.params = params
    study.objective = dummy_objective

    # Verify if study evaluates the objective
    result = study._evaluate(action_vector)
    assert result == dummy_objective(**exp_solution)
