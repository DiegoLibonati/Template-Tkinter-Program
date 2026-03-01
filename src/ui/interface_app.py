from tkinter import Tk

from src.configs.default_config import DefaultConfig
from src.models.user_model import UserModel
from src.services.auth_service import AuthService
from src.ui.styles import Styles
from src.ui.views.login_view import LoginView
from src.ui.views.main_view import MainView
from src.ui.views.register_view import RegisterView


class InterfaceApp:
    def __init__(self, root: Tk, config: DefaultConfig, styles: Styles = Styles()) -> None:
        self.user: UserModel | None = None

        self._styles = styles
        self._config = config
        self._root = root
        self._root.title("Template Tkinter")
        self._root.geometry("400x400")
        self._root.resizable(False, False)
        self._root.config(background=self._styles.PRIMARY_COLOR)

        self._login_view = LoginView(
            root=self._root,
            styles=self._styles,
            on_login=self._login,
            on_register=self._open_register,
        )
        self._login_view.pack(fill="both", expand=True)

    @property
    def username(self) -> str:
        return self.user.username if self.user else "N/A"

    def _login(self) -> None:
        username = self._login_view.text_username.get()
        password = self._login_view.text_password.get()
        user, msg = AuthService.login(username=username, password=password)

        if not user:
            self._login_view.text_confirm.set(msg)
            return

        self.user = user
        MainView(root=self._root, styles=self._styles, username=self.username)

    def _open_register(self) -> None:
        self._register_view = RegisterView(
            root=self._root,
            styles=self._styles,
            on_register=self._register,
        )

    def _register(self) -> None:
        ok, msg = AuthService.register(
            username=self._register_view.text_username.get(),
            password=self._register_view.text_password.get(),
            confirm_password=self._register_view.text_confirm_password.get(),
        )
        self._register_view.text_confirm.set(msg)
        if ok:
            self._register_view.destroy()
