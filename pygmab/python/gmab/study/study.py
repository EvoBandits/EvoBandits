from collections.abc import Callable

from gmab import logging
from gmab.config.config import Configurator
from gmab.gmab import Gmab

_logger = logging.get_logger(__name__)


class Study:
    """A Study corresponds to an optimization task, i.e. a set of trials.

    This objecht provides interfaces to optimize an objective within its bounds,
    and to set/get attributes of the study itself that are user-defined.

    Note that the direct use of this constructor is not recommended.
    Instead, use :func:`~gmab.initialize`.
    """

    def __init__(self, config: Configurator) -> None:
        self._config: Configurator = config
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

    def optimize(
        self,
        func: Callable,
        n_simulations: int,
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
            n_simulations:
                The number of simulations per trial. A trial will continue until the
                number of elapsed simulations reaches `n_simulations`.
        """
        gmab = Gmab(func, self._config.bounds)
        self._best_trial = gmab.optimize(n_simulations)
        _logger.info("completed")
