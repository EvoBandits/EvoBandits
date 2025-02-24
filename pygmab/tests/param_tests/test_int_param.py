import pytest
from gmab.params import IntParam

xValueErr = pytest.mark.xfail(raises=ValueError)


@pytest.mark.parametrize(
    "low, high, kwargs, exp_bounds, action, exp_value",
    [
        pytest.param(0, 1, {}, [(0, 1)], [1], 1, id="base"),
        pytest.param(0, 1, {"size": 2}, [(0, 1), (0, 1)], [1, 1], [1, 1], id="vector"),
        pytest.param(3, 6, {"step": 3}, [(3, 4)], [1], 6, id="step"),
        pytest.param(0, 4, {"step": 3}, [(0, 2)], [2], 4, id="step_edge_case"),
        pytest.param(0.0, 1, {}, None, None, None, marks=xValueErr, id="f_type_low"),
        pytest.param(0, 1.0, {}, None, None, None, marks=xValueErr, id="f_type_high"),
        pytest.param(0, 0, {}, None, None, None, marks=xValueErr, id="f_value_low_high"),
        pytest.param(0, 1, {"size": 2.0}, None, None, None, marks=xValueErr, id="f_type_size"),
        pytest.param(0, 4, {"step": 2.0}, None, None, None, marks=xValueErr, id="f_type_step"),
        pytest.param(0, 1, {"size": 0}, None, None, None, marks=xValueErr, id="f_value_size"),
        pytest.param(0, 4, {"step": 0}, None, None, None, marks=xValueErr, id="f_value_step"),
    ],
)
def test_int_param(low, high, kwargs, exp_bounds, action, exp_value):
    param = IntParam(low, high, **kwargs)
    assert param.bounds == exp_bounds
    assert param.map_to_value(action) == exp_value
