import importlib.util

from evobandits import logging
from evobandits.evobandits import EvoBandits
from evobandits.params import CategoricalParam, FloatParam, IntParam
from evobandits.study import ALGORITHM_DEFAULT, Study

__all__ = [
    "ALGORITHM_DEFAULT",
    "EvoBandits",
    "logging",
    "Study",
    "CategoricalParam",
    "FloatParam",
    "IntParam",
]

if importlib.util.find_spec("sklearn") is not None:
    # Only import and expose EvoBanditsSearchCV if sklearn is available
    from evobandits.search import EvoBanditsSearchCV  # noqa

    __all__.append("EvoBanditsSearchCV")
