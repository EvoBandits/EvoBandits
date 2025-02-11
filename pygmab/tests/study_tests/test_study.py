import pytest
from gmab import Study, create_study
from pytest import LogCaptureFixture


def rosenbrock_function(number: list):
    return sum(
        [
            100 * (number[i + 1] - number[i] ** 2) ** 2 + (1 - number[i]) ** 2
            for i in range(len(number) - 1)
        ]
    )


@pytest.mark.parametrize(
    "seed, expected_warning",
    [
        pytest.param(42, "", id="base"),
        pytest.param(None, "Seed not provided", id="unseeded"),
    ],
)
def test_create_study(seed, expected_warning, caplog: LogCaptureFixture):
    study = create_study(seed)
    assert isinstance(study, Study)
    assert expected_warning in caplog.text


@pytest.mark.parametrize(
    "seed, skip_optimize, expected_info",
    [
        pytest.param(42, False, "completed", id="base"),
        pytest.param(
            42,
            True,
            "",
            marks=pytest.mark.xfail(raises=RuntimeError),
            id="skip_optimization",
        ),
    ],
)
def test_best_trial(seed, skip_optimize, expected_info, caplog: LogCaptureFixture):
    study = create_study(seed)

    if not skip_optimize:
        bounds = [(-5, 10), (-5, 10)]
        n_simulations = 10_000
        study.optimize(rosenbrock_function, bounds, n_simulations)
        assert expected_info in caplog.text

    result = study.best_trial
    assert result == [1, 1]
