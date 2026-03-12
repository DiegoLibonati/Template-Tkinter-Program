from src.configs.logger_config import setup_logger
from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_USERNAME,
    MESSAGE_NOT_EXISTS_USER,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_NOT_VALID_MATCH_PASSWORD,
    MESSAGE_NOT_VALID_PASSWORD,
    MESSAGE_SUCCESS_LOGIN,
    MESSAGE_SUCCESS_REGISTER,
)
from src.data_access.user_dao import UserDAO
from src.models.user_model import UserModel
from src.services.hash_service import HashService
from src.utils.dialogs import ConflictDialogError, NotFoundDialogError, SuccessDialogInformation, ValidationDialogError

logger = setup_logger("tkinter-app - auth_service.py")


class AuthService:
    @staticmethod
    def login(username: str, password: str) -> UserModel:
        if not username or not password or username.isspace() or password.isspace():
            raise ValidationDialogError(message=MESSAGE_NOT_VALID_FIELDS)

        user = UserDAO().get_by_username(username)

        if not user:
            raise NotFoundDialogError(message=MESSAGE_NOT_EXISTS_USER)

        if not HashService.verify(password, user.password):
            raise ValidationDialogError(message=MESSAGE_NOT_VALID_PASSWORD)

        SuccessDialogInformation(message=MESSAGE_SUCCESS_LOGIN).open()
        return user

    @staticmethod
    def register(username: str, password: str, confirm_password: str) -> bool:
        if not username or not password or not confirm_password or username.isspace() or password.isspace():
            raise ValidationDialogError(message=MESSAGE_NOT_VALID_FIELDS)

        if password != confirm_password:
            raise ValidationDialogError(message=MESSAGE_NOT_VALID_MATCH_PASSWORD)

        if UserDAO().exists(username):
            raise ConflictDialogError(message=MESSAGE_ALREADY_EXISTS_USERNAME)

        user = UserModel(username=username, password=HashService.hash(password))

        UserDAO().save(user)

        SuccessDialogInformation(message=MESSAGE_SUCCESS_REGISTER).open()
        return True
