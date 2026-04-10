from unittest.mock import MagicMock, patch

from src.utils.dialogs import InternalDialogError, ValidationDialogError
from src.utils.error_handler import error_handler


class TestErrorHandler:
    def test_base_dialog_exception_calls_open(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="bad input")
        with patch.object(exc, "open") as mock_open:
            error_handler(type(exc), exc, None)  # type: ignore[arg-type]
        mock_open.assert_called_once()

    def test_internal_dialog_error_calls_open(self) -> None:
        exc: InternalDialogError = InternalDialogError(message="internal")
        with patch.object(exc, "open") as mock_open:
            error_handler(type(exc), exc, None)  # type: ignore[arg-type]
        mock_open.assert_called_once()

    def test_non_base_dialog_creates_internal_error(self) -> None:
        exc: ValueError = ValueError("something went wrong")
        with patch("src.utils.error_handler.InternalDialogError") as mock_cls:
            mock_instance: MagicMock = MagicMock()
            mock_cls.return_value = mock_instance
            error_handler(type(exc), exc, None)  # type: ignore[arg-type]
        mock_cls.assert_called_once_with(message="something went wrong")
        mock_instance.open.assert_called_once()

    def test_non_base_dialog_passes_exception_message(self) -> None:
        exc: RuntimeError = RuntimeError("runtime failure")
        with patch("src.utils.error_handler.InternalDialogError") as mock_cls:
            mock_instance: MagicMock = MagicMock()
            mock_cls.return_value = mock_instance
            error_handler(type(exc), exc, None)  # type: ignore[arg-type]
        mock_cls.assert_called_once_with(message="runtime failure")
