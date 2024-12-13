from bcrypt import hashpw, gensalt


def hash_password(password: str) -> str:
    salt = gensalt()
    hashed_password = hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return hashpw(
        password.encode("utf-8"), hashed_password.encode("utf-8")
    ) == hashed_password.encode("utf-8")
