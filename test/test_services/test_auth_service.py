from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_USERNAME,
    MESSAGE_NOT_EXISTS_USER,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_NOT_VALID_MATCH_PASSWORD,
    MESSAGE_NOT_VALID_PASSWORD,
    MESSAGE_SUCCESS_LOGIN,
    MESSAGE_SUCCESS_REGISTER,
)
from src.models.user_model import UserModel
from src.services.auth_service import AuthService
from src.utils.dialogs import ConflictDialogError, NotFoundDialogError, ValidationDialogError


class TestAuthServiceLogin:
    def test_raises_validation_error_when_username_is_empty(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.login(username="", password="pass")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_password_is_empty(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.login(username="user", password="")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_username_is_whitespace(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.login(username="   ", password="pass")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_password_is_whitespace(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.login(username="user", password="   ")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_not_found_error_when_user_does_not_exist(self, invalid_credentials: dict[str, str]) -> None:
        with patch("src.services.auth_service.UserDAO") as mock_dao_class:
            mock_dao_class.return_value.get_by_username.return_value = None
            with pytest.raises(NotFoundDialogError) as exc_info:
                AuthService.login(**invalid_credentials)
        assert exc_info.value.message == MESSAGE_NOT_EXISTS_USER

    def test_raises_validation_error_when_password_is_wrong(self, sample_user: UserModel) -> None:
        with patch("src.services.auth_service.UserDAO") as mock_dao_class:
            mock_dao_class.return_value.get_by_username.return_value = sample_user
            with pytest.raises(ValidationDialogError) as exc_info:
                AuthService.login(username="testuser", password="wrongpass")
        assert exc_info.value.message == MESSAGE_NOT_VALID_PASSWORD

    def test_returns_user_on_success(self, sample_user: UserModel) -> None:
        with (
            patch("src.services.auth_service.UserDAO") as mock_dao_class,
            patch("src.services.auth_service.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dao_class.return_value.get_by_username.return_value = sample_user
            mock_dialog_class.return_value = MagicMock()
            result: UserModel = AuthService.login(username="testuser", password="testpass")

        assert result is sample_user

    def test_success_dialog_opened_on_login(self, sample_user: UserModel) -> None:
        with (
            patch("src.services.auth_service.UserDAO") as mock_dao_class,
            patch("src.services.auth_service.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dao_class.return_value.get_by_username.return_value = sample_user
            mock_dialog: MagicMock = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            AuthService.login(username="testuser", password="testpass")

        mock_dialog_class.assert_called_once_with(message=MESSAGE_SUCCESS_LOGIN)
        mock_dialog.open.assert_called_once()

    def test_get_by_username_called_with_correct_username(self) -> None:
        with patch("src.services.auth_service.UserDAO") as mock_dao_class:
            mock_dao_class.return_value.get_by_username.return_value = None
            try:
                AuthService.login(username="testuser", password="pass")
            except NotFoundDialogError:
                pass

        mock_dao_class.return_value.get_by_username.assert_called_once_with("testuser")


class TestAuthServiceRegister:
    def test_raises_validation_error_when_username_is_empty(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.register(username="", password="pass", confirm_password="pass")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_password_is_empty(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.register(username="user", password="", confirm_password="pass")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_confirm_password_is_empty(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.register(username="user", password="pass", confirm_password="")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_username_is_whitespace(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.register(username="   ", password="pass", confirm_password="pass")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_password_is_whitespace(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.register(username="user", password="   ", confirm_password="   ")
        assert exc_info.value.message == MESSAGE_NOT_VALID_FIELDS

    def test_raises_validation_error_when_passwords_do_not_match(self) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            AuthService.register(username="user", password="pass1", confirm_password="pass2")
        assert exc_info.value.message == MESSAGE_NOT_VALID_MATCH_PASSWORD

    def test_raises_conflict_error_when_username_already_exists(self, registration_data: dict[str, str]) -> None:
        with patch("src.services.auth_service.UserDAO") as mock_dao_class:
            mock_dao_class.return_value.exists.return_value = True
            with pytest.raises(ConflictDialogError) as exc_info:
                AuthService.register(**registration_data)
        assert exc_info.value.message == MESSAGE_ALREADY_EXISTS_USERNAME

    def test_returns_true_on_success(self, registration_data: dict[str, str]) -> None:
        with (
            patch("src.services.auth_service.UserDAO") as mock_dao_class,
            patch("src.services.auth_service.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dao_class.return_value.exists.return_value = False
            mock_dialog_class.return_value = MagicMock()
            result: bool = AuthService.register(**registration_data)

        assert result is True

    def test_user_is_saved_on_success(self, registration_data: dict[str, str]) -> None:
        with (
            patch("src.services.auth_service.UserDAO") as mock_dao_class,
            patch("src.services.auth_service.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dao_class.return_value.exists.return_value = False
            mock_dialog_class.return_value = MagicMock()
            AuthService.register(**registration_data)

        mock_dao_class.return_value.save.assert_called_once()

    def test_saved_user_has_correct_username(self, registration_data: dict[str, str]) -> None:
        with (
            patch("src.services.auth_service.UserDAO") as mock_dao_class,
            patch("src.services.auth_service.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dao_class.return_value.exists.return_value = False
            mock_dialog_class.return_value = MagicMock()
            AuthService.register(**registration_data)

        saved_user: UserModel = mock_dao_class.return_value.save.call_args[0][0]
        assert saved_user.username == registration_data["username"]

    def test_saved_user_has_hashed_password(self, registration_data: dict[str, str]) -> None:
        with (
            patch("src.services.auth_service.UserDAO") as mock_dao_class,
            patch("src.services.auth_service.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dao_class.return_value.exists.return_value = False
            mock_dialog_class.return_value = MagicMock()
            AuthService.register(**registration_data)

        saved_user: UserModel = mock_dao_class.return_value.save.call_args[0][0]
        assert saved_user.password != registration_data["password"]

    def test_success_dialog_opened_on_register(self, registration_data: dict[str, str]) -> None:
        with (
            patch("src.services.auth_service.UserDAO") as mock_dao_class,
            patch("src.services.auth_service.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dao_class.return_value.exists.return_value = False
            mock_dialog: MagicMock = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            AuthService.register(**registration_data)

        mock_dialog_class.assert_called_once_with(message=MESSAGE_SUCCESS_REGISTER)
        mock_dialog.open.assert_called_once()
