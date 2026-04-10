import logging

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-returns")
        assert isinstance(logger, logging.Logger)

    def test_logger_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-level")
        assert logger.level == logging.DEBUG

    def test_logger_has_at_least_one_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-handler")
        assert len(logger.handlers) > 0

    def test_default_name_is_tkinter_app(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "tkinter-app"

    def test_same_name_returns_same_instance(self) -> None:
        logger1: logging.Logger = setup_logger("test-logger-same-name")
        logger2: logging.Logger = setup_logger("test-logger-same-name")
        assert logger1 is logger2

    def test_calling_twice_does_not_duplicate_handlers(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-no-dup")
        count_before: int = len(logger.handlers)
        setup_logger("test-logger-no-dup")
        assert len(logger.handlers) == count_before
