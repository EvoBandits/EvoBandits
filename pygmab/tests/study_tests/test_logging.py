import _pytest
import _pytest.logging
from gmab import logging


def test_get_logger(caplog: _pytest.logging.LogCaptureFixture) -> None:
    _logger = logging.get_logger("gmab.foo")
    with caplog.at_level(logging.INFO, logger="gmab.foo"):
        _logger.info("hello")
    assert "hello" in caplog.text
