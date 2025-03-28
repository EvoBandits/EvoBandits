import pytest
from gmab import Gmab


def function(number: list) -> float:
    return sum([i**2 for i in number])


def test_gmab_new():
    with pytest.raises(RuntimeError) as err:
        bounds = [(0, 1), (0, 1)]  # less than 20 combinations
        _ = Gmab(function, bounds)

    exp_msg = "population_size"
    assert exp_msg in str(err.value)
