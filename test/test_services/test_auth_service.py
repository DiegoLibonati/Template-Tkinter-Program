from src.constants.messages import (
    MESSAGE_ERROR_NOT_VALID_FIELDS,
    MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD,
    MESSAGE_ERROR_NOT_VALID_PASSWORD,
    MESSAGE_ERROR_USER_NOT_EXISTS,
    MESSAGE_ERROR_USERNAME_ALREADY_EXISTS,
    MESSAGE_SUCCESS_LOGIN,
    MESSAGE_SUCCESS_REGISTER,
)
from src.models.user_model import UserModel
from src.services.auth_service import AuthService


class TestAuthServiceLogin:
    def test_valid_credentials_returns_user_and_success_message(self, valid_credentials: dict[str, str]) -> None:
        user, msg = AuthService.login(**valid_credentials)

        assert user is not None
        assert isinstance(user, UserModel)
        assert msg == MESSAGE_SUCCESS_LOGIN

    def test_valid_credentials_returns_correct_username(self, valid_credentials: dict[str, str]) -> None:
        user, _ = AuthService.login(**valid_credentials)

        assert user is not None
        assert user.username == valid_credentials["username"]

    def test_nonexistent_user_returns_none_and_error(self, invalid_credentials: dict[str, str]) -> None:
        user, msg = AuthService.login(**invalid_credentials)

        assert user is None
        assert msg == MESSAGE_ERROR_USER_NOT_EXISTS

    def test_wrong_password_returns_none_and_error(self) -> None:
        user, msg = AuthService.login(username="pepe", password="wrongpass")

        assert user is None
        assert msg == MESSAGE_ERROR_NOT_VALID_PASSWORD

    def test_empty_username_returns_none_and_invalid_fields(self) -> None:
        user, msg = AuthService.login(username="", password="12345")

        assert user is None
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS

    def test_empty_password_returns_none_and_invalid_fields(self) -> None:
        user, msg = AuthService.login(username="pepe", password="")

        assert user is None
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS

    def test_whitespace_username_returns_none_and_invalid_fields(self) -> None:
        user, msg = AuthService.login(username="   ", password="12345")

        assert user is None
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS

    def test_whitespace_password_returns_none_and_invalid_fields(self) -> None:
        user, msg = AuthService.login(username="pepe", password="   ")

        assert user is None
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS


class TestAuthServiceRegister:
    def test_valid_registration_returns_true_and_success_message(self, registration_data: dict[str, str]) -> None:
        ok, msg = AuthService.register(**registration_data)

        assert ok is True
        assert msg == MESSAGE_SUCCESS_REGISTER

    def test_existing_username_returns_false_and_error(self) -> None:
        ok, msg = AuthService.register(username="pepe", password="12345", confirm_password="12345")

        assert ok is False
        assert msg == MESSAGE_ERROR_USERNAME_ALREADY_EXISTS

    def test_password_mismatch_returns_false_and_error(self) -> None:
        ok, msg = AuthService.register(username="newuser", password="pass1", confirm_password="pass2")

        assert ok is False
        assert msg == MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD

    def test_empty_username_returns_false_and_invalid_fields(self) -> None:
        ok, msg = AuthService.register(username="", password="pass", confirm_password="pass")

        assert ok is False
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS

    def test_empty_password_returns_false_and_invalid_fields(self) -> None:
        ok, msg = AuthService.register(username="newuser", password="", confirm_password="")

        assert ok is False
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS

    def test_whitespace_username_returns_false_and_invalid_fields(self) -> None:
        ok, msg = AuthService.register(username="   ", password="pass", confirm_password="pass")

        assert ok is False
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS

    def test_whitespace_password_returns_false_and_invalid_fields(self) -> None:
        ok, msg = AuthService.register(username="newuser", password="   ", confirm_password="   ")

        assert ok is False
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS

    def test_empty_confirm_password_returns_false_and_invalid_fields(self) -> None:
        ok, msg = AuthService.register(username="newuser", password="pass", confirm_password="")

        assert ok is False
        assert msg == MESSAGE_ERROR_NOT_VALID_FIELDS
