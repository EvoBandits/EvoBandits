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


def test_gmab_seeding():
    bounds = [(0, 100), (0, 100)]
    budget = 1
    seed = 42
    gmab = Gmab(function, bounds, seed)
    result = gmab.optimize(budget)

    same_gmab = Gmab(function, bounds, seed)
    same_result = same_gmab.optimize(budget)
    assert result == same_result

    different_gmab = Gmab(function, bounds, seed + 1)
    different_result = different_gmab.optimize(budget)
    assert result != different_result
