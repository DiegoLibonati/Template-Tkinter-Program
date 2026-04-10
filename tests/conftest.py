import tkinter as tk

import pytest

from src.data_access.user_dao import UserDAO
from src.services.auth_service import AuthService
from src.ui.styles import Styles


@pytest.fixture(scope="session", autouse=True)
def root() -> tk.Tk:
    instance: tk.Tk = tk.Tk()
    instance.withdraw()
    yield instance
    instance.destroy()


@pytest.fixture(scope="session")
def styles() -> Styles:
    return Styles()


@pytest.fixture(scope="function")
def user_dao() -> UserDAO:
    return UserDAO()


@pytest.fixture(scope="function")
def auth_service(user_dao: UserDAO) -> AuthService:
    return AuthService(dao=user_dao)
