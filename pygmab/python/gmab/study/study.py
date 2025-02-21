from collections.abc import Callable

from gmab import logging
from gmab.gmab import Gmab
from gmab.params import IntParam

_logger = logging.get_logger(__name__)


class Study:
    """A Study corresponds to an optimization task, i.e. a set of trials.

    This objecht provides interfaces to optimize an objective within its bounds,
    and to set/get attributes of the study itself that are user-defined.

    Note that the direct use of this constructor is not recommended.
    To create a study, use :func:`~gmab.create_study`.

    """

    def __init__(self, algorithm=Gmab) -> None:
        self._algorithm = algorithm
        self._params: dict | None = None
        self._func: Callable | None = None
        self._best_trial: dict | None = None

    @property
    def best_trial(self) -> dict:
        """Return the parameters of the best trial in the study.

        Returns:
            A dictionary containing parameters of the best trial.

        """
        if not self._best_trial:
            raise RuntimeError("best_trial is not available yet. Run study.optimize().")
        return self._best_trial

    # Set up the mapping
    def _run_trial(self, action_vector: list) -> float:
        kwargs = {}
        idx = 0
        for key, param in self._params.items():
            kwargs[key] = param.map(action_vector[idx : idx + param.size])
            idx += param.size
        return self._func(**kwargs)

    def optimize(
        self,
        func: Callable,
        params: dict,
        trials: int,
    ) -> None:
        """Optimize an objective function.

        Optimization is done by choosing a suitable set of hyperparmeter values within
        given ``bounds``

        The optimization trial will be stopped after ``n_simulations`` of the
        :func:`func`.

        Args:
            func:
                A callable that implements the objective function.
            bounds:
                A list of of tuples that define the bounds for each decision variable.
            trials:
                The number of simulations. An optimization will continue until the
                number of elapsed simulations reaches `trials`.
        """

        # Collect the bounds from params.
        bounds = []
        for key, param in params.items():
            assert isinstance(param, IntParam), f"{key} is not valid. Try gmab.suggest_int."
            bounds += param.bounds
        self._params = params
        self._func = func

        # Execute
        gmab = self._algorithm(self._run_trial, bounds)
        self._best_trial = gmab.optimize(trials)
        _logger.info("completed")


def create_study() -> Study:
    """Create a new :class:`~gmab.study.Study`."""
    return Study()
