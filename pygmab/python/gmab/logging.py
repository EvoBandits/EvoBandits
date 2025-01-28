# from __future__ import annotations

import logging
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

# import os
# import sys

__all__ = [
    "CRITICAL",
    "DEBUG",
    "ERROR",
    "INFO",
    "WARNING",
]

_default_handler: logging.Handler | None = None
_default_fmt: str = "[%(asctime)s] %(levelname)-8s - %(name)s - %(message)s"


def _get_library_root_logger() -> logging.Logger:
    return logging.getLogger(__name__.split(".")[0])


def _configure_library_root_logger() -> None:
    global _default_handler

    if _default_handler:
        return  # This library has already configured the library root logger.

    _default_handler = logging.StreamHandler()  # Set sys.stderr as stream.
    _default_handler.setFormatter(logging.Formatter(_default_fmt))
    library_root_logger: logging.Logger = _get_library_root_logger()
    library_root_logger.addHandler(_default_handler)
    library_root_logger.setLevel(logging.INFO)
    # library_root_logger.propagate = False


# def _reset_library_root_logger() -> None:
#     global _default_handler

#     with _lock:
#         if not _default_handler:
#             return

#         library_root_logger: logging.Logger = _get_library_root_logger()
#         library_root_logger.removeHandler(_default_handler)
#         library_root_logger.setLevel(logging.NOTSET)
#         _default_handler = None


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the specified name."""
    _configure_library_root_logger()
    return logging.getLogger(name)


# def get_verbosity() -> int:
#     """Return the current level for the Optuna's root logger.

#     Example:

#         Get the default verbosity level.

#         .. testsetup::

#             def objective(trial):
#                 x = trial.suggest_float("x", -100, 100)
#                 y = trial.suggest_categorical("y", [-1, 0, 1])
#                 return x**2 + y

#         .. testcode::

#             import optuna

#             # The default verbosity level of Optuna is `optuna.logging.INFO`.
#             print(optuna.logging.get_verbosity())
#             # 20
#             print(optuna.logging.INFO)
#             # 20

#             # There are logs of the INFO level.
#             study = optuna.create_study()
#             study.optimize(objective, n_trials=5)
#             # [I 2021-10-31 05:35:17,232] A new study created ...
#             # [I 2021-10-31 05:35:17,238] Trial 0 finished with value: ...
#             # [I 2021-10-31 05:35:17,245] Trial 1 finished with value: ...
#             # ...

#         .. testoutput::
#            :hide:

#            20
#            20
#     Returns:
#         Logging level, e.g., ``optuna.logging.DEBUG`` and ``optuna.logging.INFO``.

#     .. note::
#         Optuna has following logging levels:

#         - ``optuna.logging.CRITICAL``, ``optuna.logging.FATAL``
#         - ``optuna.logging.ERROR``
#         - ``optuna.logging.WARNING``, ``optuna.logging.WARN``
#         - ``optuna.logging.INFO``
#         - ``optuna.logging.DEBUG``
#     """

#     _configure_library_root_logger()
#     return _get_library_root_logger().getEffectiveLevel()


def set_level(level: int) -> None:
    """Set the level for gmab's root logger.

    Args:
        verbosity:
            Logging level, e.g., ``gmab.logging.DEBUG`` or ``gmab.logging.INFO``.

    """
    _configure_library_root_logger()
    _get_library_root_logger().setLevel(level)


def disable() -> None:
    """Disable the default handler of gmab's root logger"""
    _configure_library_root_logger()
    assert _default_handler is not None
    _get_library_root_logger().removeHandler(_default_handler)


def enable() -> None:
    """Enable the default handler of gmab's root logger"""
    _configure_library_root_logger()
    assert _default_handler is not None
    _get_library_root_logger().addHandler(_default_handler)
