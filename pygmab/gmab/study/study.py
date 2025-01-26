from collections.abc import Callable

from gmab import Gmab


class Study:
    def __init__(self, study_name: str | None = None) -> None:
        self.study_name: str | None = study_name
        self._best_trial: dict | None = None

    @property
    def best_trial(self) -> dict:
        if not self._best_trial:
            raise RuntimeError("best_trial is not available yet. Run study.optimize().")
        return self._best_trial

    def optimize(
        self,
        objective: Callable,
        bounds: list[tuple],
        n_simulations: int,
    ) -> None:
        gmab = Gmab(objective, bounds)
        self._best_trial = gmab.optimize(n_simulations)


def create_study(study_name: str | None = None) -> Study:
    return Study(study_name)
