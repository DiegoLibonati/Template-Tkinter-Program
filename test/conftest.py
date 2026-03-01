from tkinter import StringVar
from unittest.mock import MagicMock

import pytest

from src.models.user_model import UserModel
from src.services.hash_service import HashService

# ============================================================================
# Model fixtures
# ============================================================================


@pytest.fixture
def sample_user() -> UserModel:
    return UserModel(username="testuser", password=HashService.hash("testpass"))


@pytest.fixture
def sample_users() -> list[UserModel]:
    return [
        UserModel(username="user1", password=HashService.hash("pass1")),
        UserModel(username="user2", password=HashService.hash("pass2")),
        UserModel(username="user3", password=HashService.hash("pass3")),
    ]


# ============================================================================
# Test data fixtures
# ============================================================================


@pytest.fixture
def valid_credentials() -> dict[str, str]:
    return {"username": "pepe", "password": "12345"}


@pytest.fixture
def invalid_credentials() -> dict[str, str]:
    return {"username": "nonexistent", "password": "wrongpass"}


@pytest.fixture
def registration_data() -> dict[str, str]:
    return {
        "username": "newuser",
        "password": "newpass123",
        "confirm_password": "newpass123",
    }


# ============================================================================
# UI fixtures
# ============================================================================


@pytest.fixture
def mock_root() -> MagicMock:
    root = MagicMock()
    root.title = MagicMock()
    root.geometry = MagicMock()
    root.resizable = MagicMock()
    root.config = MagicMock()
    return root


@pytest.fixture
def mock_styles() -> MagicMock:
    styles = MagicMock()
    styles.PRIMARY_COLOR = "#ffffff"
    return styles


@pytest.fixture
def on_register() -> MagicMock:
    return MagicMock()


@pytest.fixture
def variable() -> MagicMock:
    return MagicMock(spec=StringVar)
