import hashlib

from passlib.context import CryptContext


class HashService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_hash_password(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_hash(cls, string: str):
        hash = hashlib.sha256(string.encode())
        return hash.hexdigest()

    @classmethod
    def is_valide_hash(cls, string: str, hash: str):
        hash_string = cls.create_hash(string)
        print(hash)
        print(hash_string)
        return hash_string == hash
