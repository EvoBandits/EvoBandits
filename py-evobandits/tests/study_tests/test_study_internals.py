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
    study.params = params

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
    study.params = params
    study.objective = dummy_objective
    study._direction = kwargs.get("_direction", 1)

    # Verify if study evaluates the objective
    result = study._evaluate(action_vector)
    assert result == exp_result
