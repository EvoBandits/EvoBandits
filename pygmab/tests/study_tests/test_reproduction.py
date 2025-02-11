import gmab
import pytest

from tests._functions import rosenbrock


@pytest.mark.parametrize(
    "seed, objective, bounds",
    [pytest.param(42, rosenbrock.objective, rosenbrock.BOUNDS_2D, id="base")],
)
def test_reproduction(seed, objective, bounds):
    def execute_study(seed, objective, bounds):
        study = gmab.create_study(seed)
        study.optimize(objective, bounds, n_simulations=1000)
        return study.best_trial

    first_result = execute_study(seed, objective, bounds)
    second_result = execute_study(seed, objective, bounds)
    assert first_result == second_result
