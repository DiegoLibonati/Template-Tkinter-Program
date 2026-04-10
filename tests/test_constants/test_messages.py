from src.constants import messages


class TestMessages:
    def test_success_login(self) -> None:
        assert messages.MESSAGE_SUCCESS_LOGIN == "You have successfully logged in."

    def test_success_register(self) -> None:
        assert messages.MESSAGE_SUCCESS_REGISTER == "The user was successfully created."

    def test_error_app(self) -> None:
        assert messages.MESSAGE_ERROR_APP == "Internal error. Contact a developer."

    def test_error_pydantic(self) -> None:
        assert messages.MESSAGE_ERROR_PYDANTIC == "Pydantic error. Contact a developer."

    def test_not_valid_password(self) -> None:
        assert messages.MESSAGE_NOT_VALID_PASSWORD == "The password does not match the user entered."

    def test_not_valid_match_password(self) -> None:
        assert messages.MESSAGE_NOT_VALID_MATCH_PASSWORD == "Passwords are not the same."

    def test_not_valid_fields(self) -> None:
        assert messages.MESSAGE_NOT_VALID_FIELDS == "The fields entered are invalid."

    def test_not_exists_user(self) -> None:
        assert messages.MESSAGE_NOT_EXISTS_USER == "The entered username does not exist in our database."

    def test_already_exists_username(self) -> None:
        assert messages.MESSAGE_ALREADY_EXISTS_USERNAME == "The username already exists."

    def test_not_found_dialog_type(self) -> None:
        assert messages.MESSAGE_NOT_FOUND_DIALOG_TYPE == "The type of dialog to display is not found."
