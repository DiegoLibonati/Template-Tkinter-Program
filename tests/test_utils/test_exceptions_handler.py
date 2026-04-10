import pytest

from src.constants.messages import MESSAGE_ERROR_PYDANTIC
from src.models.user_model import UserModel
from src.utils.dialogs import ValidationDialogError
from src.utils.exceptions_handler import exceptions_handler


class TestExceptionsHandler:
    def test_return_value_passes_through(self) -> None:
        @exceptions_handler
        def fn() -> int:
            return 42

        assert fn() == 42

    def test_pydantic_validation_error_raises_validation_dialog_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            UserModel(username="", password="")

        with pytest.raises(ValidationDialogError):
            fn()

    def test_other_exceptions_propagate_unchanged(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise RuntimeError("unexpected error")

        with pytest.raises(RuntimeError, match="unexpected error"):
            fn()

    def test_preserves_function_name(self) -> None:
        @exceptions_handler
        def my_function() -> None:
            pass

        assert my_function.__name__ == "my_function"

    def test_passes_positional_and_keyword_args(self) -> None:
        @exceptions_handler
        def fn(a: int, b: int = 0) -> int:
            return a + b

        assert fn(1, b=2) == 3

    def test_none_return_value_passes_through(self) -> None:
        @exceptions_handler
        def fn() -> None:
            return None

        assert fn() is None

    def test_validation_dialog_error_message_is_pydantic_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            UserModel(username="", password="")

        with pytest.raises(ValidationDialogError) as exc_info:
            fn()
        assert exc_info.value.message == MESSAGE_ERROR_PYDANTIC
