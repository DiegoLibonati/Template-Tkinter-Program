import pytest
from pydantic import ValidationError

from src.models.user_model import UserModel


class TestUserModelCreation:
    def test_create_user_with_valid_data(self) -> None:
        user = UserModel(username="testuser", password="testpass")

        assert user.username == "testuser"
        assert user.password == "testpass"

    def test_create_user_strips_whitespace_from_username(self) -> None:
        user = UserModel(username="  testuser  ", password="testpass")

        assert user.username == "testuser"

    def test_create_user_strips_whitespace_from_password(self) -> None:
        user = UserModel(username="testuser", password="  testpass  ")

        assert user.password == "testpass"


class TestUserModelValidation:
    def test_empty_username_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="", password="testpass")

    def test_empty_password_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="testuser", password="")

    def test_whitespace_only_username_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="   ", password="testpass")

    def test_whitespace_only_password_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="testuser", password="   ")

    def test_missing_username_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(password="testpass")

    def test_missing_password_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            UserModel(username="testuser")


class TestUserModelEquality:
    def test_users_with_same_data_are_equal(self) -> None:
        user1 = UserModel(username="testuser", password="testpass")
        user2 = UserModel(username="testuser", password="testpass")

        assert user1 == user2

    def test_users_with_different_username_are_not_equal(self) -> None:
        user1 = UserModel(username="user1", password="testpass")
        user2 = UserModel(username="user2", password="testpass")

        assert user1 != user2

    def test_users_with_different_password_are_not_equal(self) -> None:
        user1 = UserModel(username="testuser", password="pass1")
        user2 = UserModel(username="testuser", password="pass2")

        assert user1 != user2
