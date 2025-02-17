from gmab import logging
from gmab.config import Configurator
from gmab.gmab import Gmab
from gmab.search import GmabSearchCV
from gmab.study import Study

__all__ = [
    "Configurator",
    "Gmab",
    "GmabSearchCV",
    "logging",
    "Study",
]


def initialize() -> tuple[Study, Configurator]:
    """Initialize gmab by creating a new :class:`~gmab.study.Study` and its
    :class:`~gmab.config.Configurator`"""
    config = Configurator()
    study = Study(config)
    return study, config
