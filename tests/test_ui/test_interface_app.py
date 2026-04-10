import tkinter as tk

from src.configs.default_config import DefaultConfig
from src.models.user_model import UserModel
from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles


class TestInterfaceApp:
    def test_instantiation(self, root: tk.Tk, styles: Styles) -> None:
        app: InterfaceApp = InterfaceApp(root=root, config=DefaultConfig(), styles=styles)
        assert app is not None

    def test_user_is_none_initially(self, root: tk.Tk, styles: Styles) -> None:
        app: InterfaceApp = InterfaceApp(root=root, config=DefaultConfig(), styles=styles)
        assert app.user is None

    def test_username_returns_na_when_no_user(self, root: tk.Tk, styles: Styles) -> None:
        app: InterfaceApp = InterfaceApp(root=root, config=DefaultConfig(), styles=styles)
        assert app.username == "N/A"

    def test_username_returns_user_username_when_set(self, root: tk.Tk, styles: Styles) -> None:
        app: InterfaceApp = InterfaceApp(root=root, config=DefaultConfig(), styles=styles)
        app.user = UserModel(username="alice", password="hashed")
        assert app.username == "alice"

    def test_default_styles_used_when_not_provided(self, root: tk.Tk) -> None:
        app: InterfaceApp = InterfaceApp(root=root, config=DefaultConfig())
        assert app is not None
