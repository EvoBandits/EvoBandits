import pytest
from gmab import create_study, trial


def rosenbrock_function(number: list):
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )


def test_best_trial():
    study = create_study()

    # best_trial requires running study.optimize()
    with pytest.raises(RuntimeError):
        result = study.best_trial

    params = {"number": trial.suggest_int("number", -5, 10, 2)}
    n_simulations = 10_000
    study.optimize(rosenbrock_function, params, n_simulations)
    result = study.best_trial
    assert result == [1, 1]
