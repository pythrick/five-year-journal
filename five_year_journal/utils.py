import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def to_camel(value: str) -> str:
    return "".join(
        word.capitalize() if idx != 0 else word
        for idx, word in enumerate(value.split("_"))
    )
