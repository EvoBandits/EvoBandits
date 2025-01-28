import _pytest
import _pytest.capture
from gmab import logging


def test_get_logger(capsys: _pytest.capture.CaptureFixture) -> None:
    logger = logging.get_logger("gmab.foo")

    logger.info("hello")
    assert "hello" in capsys.readouterr().err  # Checks logging with a simple example

    logger.debug("bye")
    assert "bye" not in capsys.readouterr().err  # DEBUG is not displayed per default


def test_set_level(capsys: _pytest.capture.CaptureFixture) -> None:
    logger = logging.get_logger("gmab.foo")

    logging.set_level(logging.DEBUG)
    logger.debug("debug_msg")
    assert "debug_msg" in capsys.readouterr().err  # level is set to DEBUG

    logging.set_level(logging.CRITICAL)
    logger.error("error_msg")
    assert "error_msg" not in capsys.readouterr().err  # level is set to CRITICAL


def test_disable(capsys: _pytest.capture.CaptureFixture) -> None:
    logger = logging.get_logger("gmab.foo")

    logging.disable()
    logger.info("hello")
    assert "hello" not in capsys.readouterr().err  # Logging is disabled

    logging.enable()
    logger.info("bye")
    assert "bye" in capsys.readouterr().err  # Logging is enabled
