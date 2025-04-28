from contextlib import nullcontext

import pytest
from evobandits.params import CategoricalParam


def dummy_func():
    pass


@pytest.mark.parametrize(
    "choices, exp_bounds, expectation",
    [
        [["a", "b"], [(0, 1)], nullcontext()],
        [[True, False], [(0, 1)], nullcontext()],
        [[1, 2], [(0, 1)], nullcontext()],
        [[1.0, 2.0], [(0, 1)], nullcontext()],
        [[dummy_func, dummy_func], [(0, 1)], nullcontext()],
        [["a", False], [(0, 1)], nullcontext()],
        [["a", "b", None], [(0, 2)], nullcontext()],
        [{"a", "b"}, None, pytest.raises(ValueError)],
        [[["a", "b"], "c"], None, pytest.raises(ValueError)],
    ],
    ids=[
        "choice_str",
        "choice_bool",
        "choice_int",
        "choice_float",
        "choice_Callable",
        "choice_mixed",
        "choice_mixed2",
        "fail_choices_type",
        "fail_choices_content",
    ],
)
def test_cat_param(choices, exp_bounds, expectation):
    with expectation:
        param = CategoricalParam(choices)

        bounds = param.bounds
        assert bounds == exp_bounds

        # Check if the exact choices are recreated using the mapping
        for idx in range(bounds[0][0], bounds[0][1] + 1):
            value = param.decode([idx])
            exp_value = choices[idx]
            assert value == exp_value
            assert isinstance(value, type(exp_value))
