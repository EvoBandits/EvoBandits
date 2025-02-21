from unittest.mock import patch

import pytest
from gmab.params import IntParam, SteppedIntParam, suggest_int

xTypeErr = pytest.mark.xfail(raises=TypeError)
xValueErr = pytest.mark.xfail(raises=ValueError)


@pytest.mark.parametrize(
    "low, high, kwargs",
    [
        pytest.param(0, 1, {}, id="base"),
        pytest.param(0, 1, {"size": 2}, id="base_vector"),
        pytest.param(0, 4, {"step": 2}, id="base_stepped"),
        pytest.param(0.0, 1, {}, marks=xTypeErr, id="f_type_low"),
        pytest.param(0, 1.0, {}, marks=xTypeErr, id="f_type_high"),
        pytest.param(0, 1, {"size": 2.0}, marks=xTypeErr, id="f_type_size"),
        pytest.param(0, 4, {"step": 2.0}, marks=xTypeErr, id="f_type_step"),
        pytest.param(0, 0, {}, marks=xValueErr, id="f_value_low_high"),
        pytest.param(0, 1, {"size": 0}, marks=xValueErr, id="f_value_size"),
        pytest.param(0, 4, {"step": 0}, marks=xValueErr, id="f_value_step"),
    ],
)
@patch("gmab.params.int_param.SteppedIntParam")
@patch("gmab.params.int_param.IntParam")
def test_suggest_int(MockIntParam, MockSteppedIntParam, low, high, kwargs):
    _ = suggest_int(low, high, **kwargs)
    size = kwargs.get("size", 1)
    step = kwargs.get("step", 1)
    if step != 1:
        MockSteppedIntParam.assert_called_once_with(low, high, size, step)
    else:
        MockIntParam.assert_called_once_with(low, high, size)


@pytest.mark.parametrize(
    "low, high, kwargs, exp_bounds, numbers, exp_mapping",
    [
        pytest.param(0, 1, {}, [(0, 1)], [1], 1, id="base"),
        pytest.param(0, 1, {"size": 2}, [(0, 1), (0, 1)], [1, 1], [1, 1], id="vector"),
    ],
)
def test_int_param(low, high, kwargs, exp_bounds, numbers, exp_mapping):
    param = IntParam(low, high, **kwargs)
    assert param.bounds == exp_bounds
    assert param.map(numbers) == exp_mapping


@pytest.mark.parametrize(
    "low, high, kwargs, exp_bounds, numbers, exp_mapping",
    [
        pytest.param(3, 6, {"step": 3}, [(0, 1)], [1], 6, id="base"),
        pytest.param(3, 6, {"step": 3, "size": 2}, [(0, 1), (0, 1)], [0, 1], [3, 6], id="base"),
        pytest.param(0, 4, {"step": 3}, [(0, 2)], [2], 4, id="edge_case"),
    ],
)
def test_stepped_int_param(low, high, kwargs, exp_bounds, numbers, exp_mapping):
    param = SteppedIntParam(low, high, **kwargs)
    assert param.bounds == exp_bounds
    assert param.map(numbers) == exp_mapping
