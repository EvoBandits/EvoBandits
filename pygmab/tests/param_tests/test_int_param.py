from unittest.mock import patch

import pytest
from gmab.params import IntParam, suggest_int

xTypeErr = pytest.mark.xfail(raises=TypeError)
xValueErr = pytest.mark.xfail(raises=ValueError)


@pytest.mark.parametrize(
    "low, high, kwargs",
    [
        pytest.param(0, 1, {}, id="base"),
        pytest.param(0, 1, {"size": 2}, id="base_vector"),
        pytest.param(0.0, 1, {}, marks=xTypeErr, id="f_type_low"),
        pytest.param(0, 1.0, {}, marks=xTypeErr, id="f_type_high"),
        pytest.param(0, 1, {"size": 2.0}, marks=xTypeErr, id="f_type_size"),
        pytest.param(0, 0, {}, marks=xValueErr, id="f_value_low_high"),
        pytest.param(0, 1, {"size": 0}, marks=xValueErr, id="f_value_size"),
    ],
)
def test_suggest_int(low, high, kwargs):
    with patch("gmab.params.int_param.IntParam") as IntParam:
        _ = suggest_int(low, high, **kwargs)
        size = kwargs.get("size", 1)
        IntParam.assert_called_once_with(low, high, size)


@pytest.mark.parametrize(
    "low, high, kwargs, expected_bounds",
    [
        pytest.param(0, 1, {}, [(0, 1)], id="base"),
        pytest.param(0, 1, {"size": 2}, [(0, 1), (0, 1)], id="base_vector"),
    ],
)
def test_int_param(low, high, kwargs, expected_bounds):
    param = IntParam(low, high, **kwargs)
    bounds = param.bounds
    assert bounds == expected_bounds
