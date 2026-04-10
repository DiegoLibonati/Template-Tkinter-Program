from unittest.mock import patch

import pytest

from src.data_access.user_dao import UserDAO
from src.models.user_model import UserModel
from src.services.auth_service import AuthService
from src.services.hash_service import HashService
from src.utils.dialogs import ConflictDialogError, NotFoundDialogError, ValidationDialogError

_PATCH_OPEN = "src.utils.dialogs.SuccessDialogInformation.open"


class TestAuthServiceLogin:
    def test_login_valid_credentials_returns_user(self, auth_service: AuthService) -> None:
        with patch(_PATCH_OPEN):
            user: UserModel = auth_service.login("pepe", "12345")
        assert user.username == "pepe"

    def test_login_returns_user_model_instance(self, auth_service: AuthService) -> None:
        with patch(_PATCH_OPEN):
            result: UserModel = auth_service.login("ash", "12345")
        assert isinstance(result, UserModel)

    def test_login_empty_username_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.login("", "12345")

    def test_login_empty_password_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.login("pepe", "")

    def test_login_whitespace_username_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.login("   ", "12345")

    def test_login_whitespace_password_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.login("pepe", "   ")

    def test_login_unknown_user_raises_not_found_error(self, auth_service: AuthService) -> None:
        with pytest.raises(NotFoundDialogError):
            auth_service.login("unknown_user", "12345")

    def test_login_wrong_password_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.login("pepe", "wrongpassword")

    def test_login_all_preloaded_users(self, auth_service: AuthService) -> None:
        for username in ("pepe", "ash", "tom"):
            with patch(_PATCH_OPEN):
                user: UserModel = auth_service.login(username, "12345")
            assert user.username == username


class TestAuthServiceRegister:
    def test_register_valid_returns_true(self, auth_service: AuthService) -> None:
        with patch(_PATCH_OPEN):
            result: bool = auth_service.register("newuser", "pass123", "pass123")
        assert result is True

    def test_register_saves_user_to_dao(self, auth_service: AuthService, user_dao: UserDAO) -> None:
        with patch(_PATCH_OPEN):
            auth_service.register("saveduser", "pass", "pass")
        assert user_dao.exists("saveduser")

    def test_register_hashes_password(self, auth_service: AuthService, user_dao: UserDAO) -> None:
        with patch(_PATCH_OPEN):
            auth_service.register("hashtest", "secret", "secret")
        user: UserModel | None = user_dao.get_by_username("hashtest")
        assert user is not None
        assert HashService.verify("secret", user.password)

    def test_register_empty_username_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.register("", "pass", "pass")

    def test_register_empty_password_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.register("user", "", "")

    def test_register_whitespace_username_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.register("   ", "pass", "pass")

    def test_register_password_mismatch_raises_validation_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ValidationDialogError):
            auth_service.register("user", "pass1", "pass2")

    def test_register_duplicate_username_raises_conflict_error(self, auth_service: AuthService) -> None:
        with pytest.raises(ConflictDialogError):
            auth_service.register("pepe", "pass", "pass")

    def test_register_new_user_can_then_login(self, auth_service: AuthService) -> None:
        with patch(_PATCH_OPEN):
            auth_service.register("loginable", "mypass", "mypass")
        with patch(_PATCH_OPEN):
            user: UserModel = auth_service.login("loginable", "mypass")
        assert user.username == "loginable"
