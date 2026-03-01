from src.configs.logger_config import setup_logger
from src.constants.messages import (
    MESSAGE_ERROR_NOT_VALID_FIELDS,
    MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD,
    MESSAGE_ERROR_NOT_VALID_PASSWORD,
    MESSAGE_ERROR_USER_NOT_EXISTS,
    MESSAGE_ERROR_USERNAME_ALREADY_EXISTS,
    MESSAGE_SUCCESS_LOGIN,
    MESSAGE_SUCCESS_REGISTER,
)
from src.data_access.user_dao import UserDAO
from src.models.user_model import UserModel
from src.services.hash_service import HashService

logger = setup_logger("tkinter-app - auth_service.py")


class AuthService:
    @staticmethod
    def login(username: str, password: str) -> tuple[UserModel | None, str]:
        if not username or not password or username.isspace() or password.isspace():
            return None, MESSAGE_ERROR_NOT_VALID_FIELDS

        user = UserDAO().get_by_username(username)

        if not user:
            return None, MESSAGE_ERROR_USER_NOT_EXISTS

        if not HashService.verify(password, user.password):
            return None, MESSAGE_ERROR_NOT_VALID_PASSWORD

        return user, MESSAGE_SUCCESS_LOGIN

    @staticmethod
    def register(username: str, password: str, confirm_password: str) -> tuple[bool, str]:
        if not username or not password or not confirm_password or username.isspace() or password.isspace():
            return False, MESSAGE_ERROR_NOT_VALID_FIELDS

        if password != confirm_password:
            return False, MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD

        if UserDAO().exists(username):
            return False, MESSAGE_ERROR_USERNAME_ALREADY_EXISTS

        user = UserModel(username=username, password=HashService.hash(password))

        UserDAO().save(user)
        logger.info(user)

        return True, MESSAGE_SUCCESS_REGISTER
