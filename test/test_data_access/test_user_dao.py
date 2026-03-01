from src.data_access.user_dao import UserDAO
from src.models.user_model import UserModel
from src.services.hash_service import HashService


class TestUserDAOGetByUsername:
    def test_get_existing_user_returns_user_model(self) -> None:
        result = UserDAO().get_by_username("pepe")

        assert result is not None
        assert isinstance(result, UserModel)
        assert result.username == "pepe"

    def test_get_nonexistent_user_returns_none(self) -> None:
        result = UserDAO().get_by_username("nonexistent")

        assert result is None

    def test_get_user_from_empty_dao_returns_none(self) -> None:
        user_dao = UserDAO()
        user_dao._users.clear()
        result = user_dao.get_by_username("pepe")

        assert result is None


class TestUserDAOExists:
    def test_existing_user_returns_true(self) -> None:
        assert UserDAO().exists("pepe") is True

    def test_nonexistent_user_returns_false(self) -> None:
        assert UserDAO().exists("nonexistent") is False

    def test_exists_is_case_sensitive(self) -> None:
        assert UserDAO().exists("pepe") is True
        assert UserDAO().exists("Pepe") is False
        assert UserDAO().exists("PEPE") is False


class TestUserDAOSave:
    def test_save_new_user(self) -> None:
        user = UserModel(username="newuser", password=HashService.hash("newpass"))
        user_dao = UserDAO()

        user_dao.save(user)

        assert user_dao.exists("newuser") is True

    def test_save_user_is_retrievable(self) -> None:
        user = UserModel(username="newuser", password=HashService.hash("newpass"))
        user_dao = UserDAO()

        user_dao.save(user)
        retrieved = user_dao.get_by_username("newuser")

        assert retrieved is not None
        assert retrieved.username == "newuser"
        assert retrieved.password == user.password

    def test_save_overwrites_existing_user(self) -> None:
        new_password = HashService.hash("updatedpass")
        updated_user = UserModel(username="pepe", password=new_password)
        user_dao = UserDAO()

        user_dao.save(updated_user)
        retrieved = user_dao.get_by_username("pepe")

        assert retrieved is not None
        assert retrieved.password == new_password

    def test_save_multiple_users(self, sample_users: list[UserModel]) -> None:
        user_dao = UserDAO()

        for user in sample_users:
            user_dao.save(user)

        for user in sample_users:
            assert user_dao.exists(user.username) is True


class TestUserDAODefaultData:
    def test_dao_has_default_users(self) -> None:
        assert UserDAO().exists("pepe") is True
        assert UserDAO().exists("ash") is True
        assert UserDAO().exists("tom") is True

    def test_dao_default_users_have_hashed_passwords(self) -> None:
        user = UserDAO().get_by_username("pepe")

        assert user is not None
        assert user.password != "12345"
        assert HashService.verify("12345", user.password) is True
