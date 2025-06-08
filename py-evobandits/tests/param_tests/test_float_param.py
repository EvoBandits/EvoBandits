# Copyright 2025 EvoBandits
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from contextlib import nullcontext

import pytest
from evobandits.params import FloatParam

test_float_param_new_data = [
    pytest.param(0, 1, {}, [(0, 100)], id="base"),
    pytest.param(0, 1, {"size": 2}, [(0, 100), (0, 100)], id="vector"),
    pytest.param(0, 1, {"n_steps": 10}, [(0, 10)], id="n_steps"),
    pytest.param(1, 2, {"log": True}, [(0, 100)], id="log"),
    pytest.param(0, 0, {"exp": pytest.raises(ValueError)}, None, id="high_value"),
    pytest.param(0, 1, {"size": 0, "exp": pytest.raises(ValueError)}, None, id="size_value"),
    pytest.param(0, 1, {"n_steps": 0, "exp": pytest.raises(ValueError)}, None, id="n_steps_value"),
    pytest.param(0, 1, {"log": True, "exp": pytest.raises(ValueError)}, None, id="log_value"),
]


@pytest.mark.parametrize("low, high, kwargs, exp_bounds", test_float_param_new_data)
def test_float_param_new(low, high, kwargs, exp_bounds):
    expectation = kwargs.pop("exp", nullcontext())
    with expectation:
        param = FloatParam(low, high, **kwargs)

        # Check evobandits's internal bounds
        bounds = param.bounds
        assert bounds == exp_bounds

        # Check if parameter maps values in the specified range
        smallest_value = param.decode([bounds[0][0]])
        assert isinstance(smallest_value, float)
        assert smallest_value == low

        largest_value = param.decode([bounds[0][1]])
        assert isinstance(largest_value, float)
        assert largest_value == high


test_float_param_mapping_data = [
    pytest.param(FloatParam(0, 1), 5, 0.05, id="base"),
    pytest.param(FloatParam(0.123, 4.567), 100, 4.567, id="modify_range"),
    pytest.param(FloatParam(0, 1, n_steps=1000), 5, 0.005, id="modify_steps"),
    pytest.param(FloatParam(1, 2, log=True), 100, 2.000, id="log_transform"),
]


@pytest.mark.parametrize("param, action, exp_value", test_float_param_mapping_data)
def test_float_param_mapping(param, action, exp_value):
    # Try multiple times to ensure precision (the exact same value should be mapped each time)
    values = []
    for _ in range(100):
        values.append(param.decode([action]))
    assert all(exp_value == x for x in values)
