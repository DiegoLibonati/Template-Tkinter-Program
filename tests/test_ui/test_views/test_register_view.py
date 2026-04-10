import tkinter as tk

from src.ui.styles import Styles
from src.ui.views.register_view import RegisterView


class TestRegisterView:
    def test_instantiation(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        assert view is not None
        view.destroy()

    def test_title_is_register(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        assert view.title() == "Register"
        view.destroy()

    def test_is_not_resizable(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        assert view.resizable() == (False, False)
        view.destroy()

    def test_text_confirm_default_is_empty(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        assert view.text_confirm.get() == ""
        view.destroy()

    def test_text_username_default_is_empty(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        assert view.text_username.get() == ""
        view.destroy()

    def test_text_password_default_is_empty(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        assert view.text_password.get() == ""
        view.destroy()

    def test_text_confirm_password_default_is_empty(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        assert view.text_confirm_password.get() == ""
        view.destroy()

    def test_text_username_set_and_get(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        view.text_username.set("bob")
        assert view.text_username.get() == "bob"
        view.destroy()

    def test_text_password_set_and_get(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        view.text_password.set("mypass")
        assert view.text_password.get() == "mypass"
        view.destroy()

    def test_text_confirm_password_set_and_get(self, root: tk.Tk, styles: Styles) -> None:
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: None)
        view.text_confirm_password.set("mypass")
        assert view.text_confirm_password.get() == "mypass"
        view.destroy()

    def test_on_register_callback_is_invoked(self, root: tk.Tk, styles: Styles) -> None:
        called: list[bool] = []
        view: RegisterView = RegisterView(root=root, styles=styles, on_register=lambda: called.append(True))
        view._on_register()
        assert called == [True]
        view.destroy()
