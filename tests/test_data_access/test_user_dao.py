from src.data_access.user_dao import UserDAO
from src.models.user_model import UserModel
from src.services.hash_service import HashService


class TestUserDAO:
    def test_initial_users_exist(self, user_dao: UserDAO) -> None:
        assert user_dao.exists("pepe")
        assert user_dao.exists("ash")
        assert user_dao.exists("tom")

    def test_get_by_username_returns_correct_user(self, user_dao: UserDAO) -> None:
        user: UserModel | None = user_dao.get_by_username("pepe")
        assert user is not None
        assert user.username == "pepe"

    def test_get_by_username_returns_none_for_unknown(self, user_dao: UserDAO) -> None:
        result: UserModel | None = user_dao.get_by_username("nonexistent_user")
        assert result is None

    def test_exists_returns_false_for_unknown(self, user_dao: UserDAO) -> None:
        assert user_dao.exists("unknown") is False

    def test_save_adds_new_user(self, user_dao: UserDAO) -> None:
        new_user: UserModel = UserModel(username="new_user", password=HashService.hash("pass"))
        user_dao.save(new_user)
        assert user_dao.exists("new_user")

    def test_save_overwrites_existing_user(self, user_dao: UserDAO) -> None:
        updated: UserModel = UserModel(username="pepe", password=HashService.hash("newpass"))
        user_dao.save(updated)
        user: UserModel | None = user_dao.get_by_username("pepe")
        assert user is not None
        assert HashService.verify("newpass", user.password)

    def test_initial_passwords_are_hashed_correctly(self, user_dao: UserDAO) -> None:
        user: UserModel | None = user_dao.get_by_username("ash")
        assert user is not None
        assert HashService.verify("12345", user.password)

    def test_get_by_username_after_save(self, user_dao: UserDAO) -> None:
        saved: UserModel = UserModel(username="alice", password=HashService.hash("secret"))
        user_dao.save(saved)
        retrieved: UserModel | None = user_dao.get_by_username("alice")
        assert retrieved is not None
        assert retrieved.username == "alice"
