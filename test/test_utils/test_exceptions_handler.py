import pytest
from pydantic import BaseModel, ValidationError

from src.constants.messages import MESSAGE_ERROR_PYDANTIC
from src.utils.dialogs import NotFoundDialogError, ValidationDialogError
from src.utils.exceptions_handler import exceptions_handler


def make_validation_error() -> ValidationError:
    class DummyModel(BaseModel):
        value: int

    try:
        DummyModel(value="not_an_int")
    except ValidationError as e:
        return e


class TestHandleExceptions:
    def test_returns_result_when_no_exception(self) -> None:
        @exceptions_handler
        def fn() -> str:
            return "ok"

        assert fn() == "ok"

    def test_raises_validation_dialog_error_on_pydantic_validation_error(self) -> None:
        validation_error: ValidationError = make_validation_error()

        @exceptions_handler
        def fn() -> None:
            raise validation_error

        with pytest.raises(ValidationDialogError) as exc_info:
            fn()

        assert exc_info.value.message == MESSAGE_ERROR_PYDANTIC

    def test_does_not_suppress_other_exceptions(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise ValueError("something else")

        with pytest.raises(ValueError, match="something else"):
            fn()

    def test_preserves_function_name(self) -> None:
        @exceptions_handler
        def my_function() -> None:
            pass

        assert my_function.__name__ == "my_function"

    def test_passes_args_to_wrapped_function(self) -> None:
        @exceptions_handler
        def fn(a: int, b: int) -> int:
            return a + b

        assert fn(2, 3) == 5

    def test_passes_kwargs_to_wrapped_function(self) -> None:
        @exceptions_handler
        def fn(a: int, b: int = 0) -> int:
            return a + b

        assert fn(a=2, b=3) == 5

    def test_does_not_suppress_base_dialog_exceptions(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise NotFoundDialogError(message="not found")

        with pytest.raises(NotFoundDialogError):
            fn()

    def test_returns_none_when_function_returns_none(self) -> None:
        @exceptions_handler
        def fn() -> None:
            return None

        assert fn() is None
