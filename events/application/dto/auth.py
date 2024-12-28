from dataclasses import dataclass


@dataclass(slots=True)
class NewUserDTO:
    email: str
    username: str
    password: str
