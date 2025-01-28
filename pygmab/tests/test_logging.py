import _pytest
import _pytest.logging
from gmab import logging


def test_get_logger(caplog: _pytest.logging.LogCaptureFixture) -> None:
    _logger = logging.get_logger("gmab.foo")
    _logger.info("hello")
    _logger.debug("bye")

    # Check if default level is logging.INFO
    assert "hello" in caplog.text
    assert "bye" not in caplog.text


def test_level(caplog: _pytest.logging.LogCaptureFixture) -> None:
    _logger = logging.get_logger("gmab.foo")

    logging.set_level(logging.DEBUG)
    _logger.debug("debug_msg")
    assert "debug_msg" in caplog.text  # Check if level has been lowered

    logging.set_level(logging.CRITICAL)
    _logger.error("error_msg")
    assert "error_msg" not in caplog.text  # Check if level has been increased
