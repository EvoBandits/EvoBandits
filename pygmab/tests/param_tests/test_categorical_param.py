from contextlib import nullcontext

import pytest
from gmab.params import CategoricalParam

test_cat_param_data = [
    pytest.param(["a", "b"], [(0, 1)], nullcontext(), id="base"),
    # For each type of choice and input errs.
]


@pytest.mark.parametrize("choices, exp_bounds, expectation", test_cat_param_data)
def test_cat_param(choices, exp_bounds, expectation):
    with expectation:
        param = CategoricalParam(choices)

        bounds = param.bounds
        assert bounds == exp_bounds

        # Check if the choices can be recreated using the mapping
        mapped_choices = []
        for x in range(bounds[0][0], bounds[0][1] + 1):
            mapped_choices.append(param.map_to_value([x]))
        assert mapped_choices == choices
