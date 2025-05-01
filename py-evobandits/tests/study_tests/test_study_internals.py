import pytest
from evobandits import IntParam
from evobandits.study.study import Study


@pytest.mark.parametrize(
    "params, exp_bounds",
    [
        [{"a": IntParam(0, 1)}, [(0, 1)]],
        [{"a": IntParam(0, 1, 2)}, [(0, 1), (0, 1)]],
        [{"a": IntParam(0, 1, 2), "b": IntParam(1, 2)}, [(0, 1), (0, 1), (1, 2)]],
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
