from src.services.hash_service import HashService


class TestHashServiceHash:
    def test_hash_returns_string(self) -> None:
        assert isinstance(HashService.hash("password"), str)

    def test_hash_is_not_plaintext(self) -> None:
        assert HashService.hash("password") != "password"

    def test_hash_is_deterministic(self) -> None:
        assert HashService.hash("password") == HashService.hash("password")

    def test_different_inputs_produce_different_hashes(self) -> None:
        assert HashService.hash("pass1") != HashService.hash("pass2")

    def test_hash_length_is_64_chars(self) -> None:
        assert len(HashService.hash("any text")) == 64

    def test_hash_empty_string(self) -> None:
        result = HashService.hash("")
        assert isinstance(result, str)
        assert len(result) == 64

    def test_hash_is_case_sensitive(self) -> None:
        assert HashService.hash("Password") != HashService.hash("password")


class TestHashServiceVerify:
    def test_verify_correct_password_returns_true(self) -> None:
        hashed = HashService.hash("mypassword")
        assert HashService.verify("mypassword", hashed) is True

    def test_verify_wrong_password_returns_false(self) -> None:
        hashed = HashService.hash("mypassword")
        assert HashService.verify("wrongpassword", hashed) is False

    def test_verify_is_case_sensitive(self) -> None:
        hashed = HashService.hash("mypassword")
        assert HashService.verify("MyPassword", hashed) is False

    def test_verify_empty_string(self) -> None:
        hashed = HashService.hash("")
        assert HashService.verify("", hashed) is True

    def test_verify_returns_bool(self) -> None:
        hashed = HashService.hash("text")
        assert isinstance(HashService.verify("text", hashed), bool)
