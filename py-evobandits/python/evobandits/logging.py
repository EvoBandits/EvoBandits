import logging
import sys
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

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

    _default_handler = logging.StreamHandler(sys.stderr)
    _default_handler.setFormatter(logging.Formatter(_default_fmt))
    library_root_logger: logging.Logger = _get_library_root_logger()
    library_root_logger.addHandler(_default_handler)
    library_root_logger.setLevel(logging.INFO)
    # library_root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the specified name."""
    _configure_library_root_logger()
    return logging.getLogger(name)


def set_level(level: int) -> None:
    """Set the level for evobandits's root logger.

    Args:
        verbosity:
            Logging level, e.g., ``evobandits.logging.DEBUG`` or ``evobandits.logging.INFO``.

    """
    _configure_library_root_logger()
    _get_library_root_logger().setLevel(level)


def disable() -> None:
    """Disable the default handler of evobandits's root logger"""
    global _default_handler
    if _default_handler:
        library_root_logger: logging.Logger = _get_library_root_logger()
        library_root_logger.removeHandler(_default_handler)
        _default_handler = None


def enable() -> None:
    """Enable the default handler of evobandits's root logger"""
    _configure_library_root_logger()
    _get_library_root_logger()
