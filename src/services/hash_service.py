import hashlib


class HashService:
    @staticmethod
    def hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def verify(text: str, hashed_text: str) -> bool:
        return HashService.hash(text) == hashed_text
