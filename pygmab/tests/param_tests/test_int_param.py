import pytest
from gmab.params import IntParam, suggest_int

xTypeErr = pytest.mark.xfail(raises=TypeError)
xValueErr = pytest.mark.xfail(raises=ValueError)


@pytest.mark.parametrize(
    "low, high, kwargs, expected_param",
    [
        pytest.param(0, 1, {}, IntParam(0, 1), id="base"),
        pytest.param(0, 1, {"size": 2}, IntParam(0, 1, 2), id="base_vector"),
        pytest.param(0.0, 1, {}, IntParam(0, 1), marks=xTypeErr, id="f_type_low"),
        pytest.param(0, 1.0, {}, IntParam(0, 1), marks=xTypeErr, id="f_type_high"),
        pytest.param(0, 1, {"size": 2.0}, IntParam(0, 1, 2), marks=xTypeErr, id="f_type_size"),
        pytest.param(0, 0, {}, None, marks=xValueErr, id="f_value_low_high"),
        pytest.param(0, 1, {"size": 0}, None, marks=xValueErr, id="f_value_size"),
    ],
)
def test_suggest_int(low, high, kwargs, expected_param):
    param = suggest_int(low, high, **kwargs)
    assert param is expected_param


@pytest.mark.parametrize(
    "param, expected_bounds",
    [
        pytest.param(suggest_int(0, 1), [(0, 1)], id="base"),
        pytest.param(suggest_int(0, 1, size=2), [(0, 1), (0, 1)], id="base_vector"),
    ],
)
def test_int_param_bounds(param, expected_bounds):
    bounds = param.bounds
    assert bounds == expected_bounds
