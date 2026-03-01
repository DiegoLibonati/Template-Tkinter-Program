from unittest.mock import MagicMock, patch

import pytest

from src.configs.testing_config import TestingConfig
from src.models.user_model import UserModel
from src.services.hash_service import HashService
from src.ui.interface_app import InterfaceApp


@pytest.fixture
def app(mock_root: MagicMock, mock_styles: MagicMock) -> InterfaceApp:
    with patch("src.ui.interface_app.LoginView") as mock_login_view_cls:
        mock_login_view = MagicMock()
        mock_login_view_cls.return_value = mock_login_view
        instance = InterfaceApp(root=mock_root, config=TestingConfig, styles=mock_styles)
        instance._login_view = mock_login_view
        return instance


class TestInterfaceAppInit:
    def test_user_is_none_on_init(self, app: InterfaceApp) -> None:
        assert app.user is None

    def test_root_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.LoginView"):
            InterfaceApp(root=mock_root, config=TestingConfig, styles=mock_styles)
        mock_root.title.assert_called_once_with("Template Tkinter")

    def test_root_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.LoginView"):
            InterfaceApp(root=mock_root, config=TestingConfig, styles=mock_styles)
        mock_root.geometry.assert_called_once_with("400x400")

    def test_root_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with patch("src.ui.interface_app.LoginView"):
            InterfaceApp(root=mock_root, config=TestingConfig, styles=mock_styles)
        mock_root.resizable.assert_called_once_with(False, False)

    def test_stores_config(self, app: InterfaceApp) -> None:
        assert app._config == TestingConfig

    def test_stores_styles(self, app: InterfaceApp, mock_styles: MagicMock) -> None:
        assert app._styles == mock_styles


class TestInterfaceAppUsername:
    def test_username_returns_na_when_no_user(self, app: InterfaceApp) -> None:
        assert app.username == "N/A"

    def test_username_returns_username_when_user_set(self, app: InterfaceApp) -> None:
        app.user = UserModel(username="pepe", password=HashService.hash("12345"))
        assert app.username == "pepe"

    def test_username_is_string(self, app: InterfaceApp) -> None:
        assert isinstance(app.username, str)


class TestInterfaceAppLogin:
    def test_successful_login_sets_user(self, app: InterfaceApp) -> None:
        app._login_view.text_username.get.return_value = "pepe"
        app._login_view.text_password.get.return_value = "12345"

        with patch("src.ui.interface_app.MainView"):
            app._login()

        assert app.user is not None
        assert app.user.username == "pepe"

    def test_successful_login_opens_main_view(self, app: InterfaceApp) -> None:
        app._login_view.text_username.get.return_value = "pepe"
        app._login_view.text_password.get.return_value = "12345"

        with patch("src.ui.interface_app.MainView") as mock_main_view:
            app._login()

        mock_main_view.assert_called_once()

    def test_failed_login_does_not_set_user(self, app: InterfaceApp) -> None:
        app._login_view.text_username.get.return_value = "nonexistent"
        app._login_view.text_password.get.return_value = "wrongpass"

        app._login()

        assert app.user is None

    def test_failed_login_sets_error_message(self, app: InterfaceApp) -> None:
        app._login_view.text_username.get.return_value = "nonexistent"
        app._login_view.text_password.get.return_value = "wrongpass"

        app._login()

        app._login_view.text_confirm.set.assert_called_once()

    def test_failed_login_does_not_open_main_view(self, app: InterfaceApp) -> None:
        app._login_view.text_username.get.return_value = "nonexistent"
        app._login_view.text_password.get.return_value = "wrongpass"

        with patch("src.ui.interface_app.MainView") as mock_main_view:
            app._login()

        mock_main_view.assert_not_called()


class TestInterfaceAppOpenRegister:
    def test_open_register_creates_register_view(self, app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.RegisterView") as mock_register_view_cls:
            app._open_register()

        mock_register_view_cls.assert_called_once()

    def test_open_register_stores_register_view(self, app: InterfaceApp) -> None:
        with patch("src.ui.interface_app.RegisterView") as mock_register_view_cls:
            mock_register_view_cls.return_value = MagicMock()
            app._open_register()

        assert hasattr(app, "_register_view")


class TestInterfaceAppRegister:
    def test_successful_register_destroys_view(self, app: InterfaceApp) -> None:
        mock_register_view = MagicMock()
        mock_register_view.text_username.get.return_value = "brandnewuser"
        mock_register_view.text_password.get.return_value = "newpass123"
        mock_register_view.text_confirm_password.get.return_value = "newpass123"
        app._register_view = mock_register_view

        app._register()

        mock_register_view.destroy.assert_called_once()

    def test_failed_register_does_not_destroy_view(self, app: InterfaceApp) -> None:
        mock_register_view = MagicMock()
        mock_register_view.text_username.get.return_value = "pepe"
        mock_register_view.text_password.get.return_value = "12345"
        mock_register_view.text_confirm_password.get.return_value = "12345"
        app._register_view = mock_register_view

        app._register()

        mock_register_view.destroy.assert_not_called()

    def test_register_sets_confirm_message(self, app: InterfaceApp) -> None:
        mock_register_view = MagicMock()
        mock_register_view.text_username.get.return_value = "brandnewuser2"
        mock_register_view.text_password.get.return_value = "newpass123"
        mock_register_view.text_confirm_password.get.return_value = "newpass123"
        app._register_view = mock_register_view

        app._register()

        mock_register_view.text_confirm.set.assert_called_once()

    def test_register_sets_error_message_on_failure(self, app: InterfaceApp) -> None:
        mock_register_view = MagicMock()
        mock_register_view.text_username.get.return_value = "pepe"
        mock_register_view.text_password.get.return_value = "pass1"
        mock_register_view.text_confirm_password.get.return_value = "pass2"
        app._register_view = mock_register_view

        app._register()

        mock_register_view.text_confirm.set.assert_called_once()
        mock_register_view.destroy.assert_not_called()
