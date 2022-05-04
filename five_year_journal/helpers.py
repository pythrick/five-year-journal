import random
import string
import uuid

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_random_string(length=32) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def to_camel(value: str) -> str:
    return "".join(
        word.capitalize() if idx != 0 else word
        for idx, word in enumerate(value.split("_"))
    )


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()
