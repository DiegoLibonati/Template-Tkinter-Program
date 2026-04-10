from src.services.hash_service import HashService


class TestHashService:
    def test_hash_returns_string(self) -> None:
        result: str = HashService.hash("hello")
        assert isinstance(result, str)

    def test_hash_is_deterministic(self) -> None:
        assert HashService.hash("hello") == HashService.hash("hello")

    def test_different_inputs_produce_different_hashes(self) -> None:
        assert HashService.hash("abc") != HashService.hash("xyz")

    def test_hash_length_is_64_characters(self) -> None:
        result: str = HashService.hash("test")
        assert len(result) == 64

    def test_verify_returns_true_for_correct_password(self) -> None:
        hashed: str = HashService.hash("mypassword")
        assert HashService.verify("mypassword", hashed) is True

    def test_verify_returns_false_for_wrong_password(self) -> None:
        hashed: str = HashService.hash("mypassword")
        assert HashService.verify("wrongpassword", hashed) is False

    def test_verify_empty_string_against_its_hash(self) -> None:
        hashed: str = HashService.hash("")
        assert HashService.verify("", hashed) is True

    def test_hash_empty_string_has_correct_length(self) -> None:
        result: str = HashService.hash("")
        assert len(result) == 64

    def test_hash_is_lowercase_hex(self) -> None:
        result: str = HashService.hash("anything")
        assert all(c in "0123456789abcdef" for c in result)
