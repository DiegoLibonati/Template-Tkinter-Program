from src.constants import messages


class TestSuccessMessages:
    def test_success_login_message(self) -> None:
        assert messages.MESSAGE_SUCCESS_LOGIN == "You have successfully logged in."

    def test_success_register_message(self) -> None:
        assert messages.MESSAGE_SUCCESS_REGISTER == "The user was successfully created."

    def test_success_messages_are_strings(self) -> None:
        assert isinstance(messages.MESSAGE_SUCCESS_LOGIN, str)
        assert isinstance(messages.MESSAGE_SUCCESS_REGISTER, str)

    def test_success_messages_are_not_empty(self) -> None:
        assert messages.MESSAGE_SUCCESS_LOGIN
        assert messages.MESSAGE_SUCCESS_REGISTER


class TestErrorMessages:
    def test_error_user_not_exists_message(self) -> None:
        assert messages.MESSAGE_ERROR_USER_NOT_EXISTS == "The entered username does not exist in our database."

    def test_error_username_already_exists_message(self) -> None:
        assert messages.MESSAGE_ERROR_USERNAME_ALREADY_EXISTS == "The username already exists."

    def test_error_not_valid_password_message(self) -> None:
        assert messages.MESSAGE_ERROR_NOT_VALID_PASSWORD == "The password does not match the user entered."

    def test_error_not_valid_match_password_message(self) -> None:
        assert messages.MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD == "Passwords are not the same."

    def test_error_not_valid_fields_message(self) -> None:
        assert messages.MESSAGE_ERROR_NOT_VALID_FIELDS == "The fields entered are invalid."

    def test_error_messages_are_strings(self) -> None:
        assert isinstance(messages.MESSAGE_ERROR_USER_NOT_EXISTS, str)
        assert isinstance(messages.MESSAGE_ERROR_USERNAME_ALREADY_EXISTS, str)
        assert isinstance(messages.MESSAGE_ERROR_NOT_VALID_PASSWORD, str)
        assert isinstance(messages.MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD, str)
        assert isinstance(messages.MESSAGE_ERROR_NOT_VALID_FIELDS, str)

    def test_error_messages_are_not_empty(self) -> None:
        assert messages.MESSAGE_ERROR_USER_NOT_EXISTS
        assert messages.MESSAGE_ERROR_USERNAME_ALREADY_EXISTS
        assert messages.MESSAGE_ERROR_NOT_VALID_PASSWORD
        assert messages.MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD
        assert messages.MESSAGE_ERROR_NOT_VALID_FIELDS


class TestMessagesUniqueness:
    def test_all_messages_are_unique(self) -> None:
        all_messages = [
            messages.MESSAGE_SUCCESS_LOGIN,
            messages.MESSAGE_SUCCESS_REGISTER,
            messages.MESSAGE_ERROR_USER_NOT_EXISTS,
            messages.MESSAGE_ERROR_USERNAME_ALREADY_EXISTS,
            messages.MESSAGE_ERROR_NOT_VALID_PASSWORD,
            messages.MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD,
            messages.MESSAGE_ERROR_NOT_VALID_FIELDS,
        ]
        assert len(all_messages) == len(set(all_messages))

    def test_success_and_error_messages_do_not_overlap(self) -> None:
        success = {messages.MESSAGE_SUCCESS_LOGIN, messages.MESSAGE_SUCCESS_REGISTER}
        errors = {
            messages.MESSAGE_ERROR_USER_NOT_EXISTS,
            messages.MESSAGE_ERROR_USERNAME_ALREADY_EXISTS,
            messages.MESSAGE_ERROR_NOT_VALID_PASSWORD,
            messages.MESSAGE_ERROR_NOT_VALID_MATCH_PASSWORD,
            messages.MESSAGE_ERROR_NOT_VALID_FIELDS,
        }
        assert success.isdisjoint(errors)
