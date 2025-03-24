from contextlib import nullcontext

import pytest
from gmab.params import IntParam

test_int_param_data = [
    pytest.param(0, 1, {}, [(0, 1)], [0, 1], id="base"),
    pytest.param(0, 1, {"size": 2}, [(0, 1), (0, 1)], [0, 1], id="vector"),
    pytest.param(3, 6, {"step": 3}, [(3, 4)], [3, 6], id="step"),
    pytest.param(3, 7, {"step": 3}, [(3, 5)], [3, 6, 7], id="step_edge_case"),
    pytest.param(0, 0, {"exp": pytest.raises(ValueError)}, None, None, id="high_value"),
    pytest.param(0, 1, {"size": 0, "exp": pytest.raises(ValueError)}, None, None, id="size_value"),
    pytest.param(0, 4, {"step": 0, "exp": pytest.raises(ValueError)}, None, None, id="step_value"),
]


@pytest.mark.parametrize("low, high, kwargs, exp_bounds, exp_values", test_int_param_data)
def test_int_param(low, high, kwargs, exp_bounds, exp_values):
    expectation = kwargs.pop("exp", nullcontext())
    with expectation:
        param = IntParam(low, high, **kwargs)

        bounds = param.bounds
        assert bounds == exp_bounds

        # Check if the expected values can be generated from the bounds
        values = []
        for x in range(bounds[0][0], bounds[0][1] + 1):
            values.append(param.map_to_value([x]))
        assert values == exp_values
