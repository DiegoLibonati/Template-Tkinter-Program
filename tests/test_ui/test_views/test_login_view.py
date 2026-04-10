import tkinter as tk

from src.ui.styles import Styles
from src.ui.views.login_view import LoginView


class TestLoginView:
    def test_instantiation(self, root: tk.Tk, styles: Styles) -> None:
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: None, on_register=lambda: None)
        assert view is not None
        view.destroy()

    def test_text_confirm_default_is_welcome(self, root: tk.Tk, styles: Styles) -> None:
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: None, on_register=lambda: None)
        assert view.text_confirm.get() == "Welcome"
        view.destroy()

    def test_text_username_default_is_empty(self, root: tk.Tk, styles: Styles) -> None:
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: None, on_register=lambda: None)
        assert view.text_username.get() == ""
        view.destroy()

    def test_text_password_default_is_empty(self, root: tk.Tk, styles: Styles) -> None:
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: None, on_register=lambda: None)
        assert view.text_password.get() == ""
        view.destroy()

    def test_text_username_set_and_get(self, root: tk.Tk, styles: Styles) -> None:
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: None, on_register=lambda: None)
        view.text_username.set("alice")
        assert view.text_username.get() == "alice"
        view.destroy()

    def test_text_password_set_and_get(self, root: tk.Tk, styles: Styles) -> None:
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: None, on_register=lambda: None)
        view.text_password.set("secret")
        assert view.text_password.get() == "secret"
        view.destroy()

    def test_on_login_callback_is_invoked(self, root: tk.Tk, styles: Styles) -> None:
        called: list[bool] = []
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: called.append(True), on_register=lambda: None)
        view._on_login()
        assert called == [True]
        view.destroy()

    def test_on_register_callback_is_invoked(self, root: tk.Tk, styles: Styles) -> None:
        called: list[bool] = []
        view: LoginView = LoginView(root=root, styles=styles, on_login=lambda: None, on_register=lambda: called.append(True))
        view._on_register()
        assert called == [True]
        view.destroy()
