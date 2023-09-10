from __future__ import annotations

from models.base import Base
from utilities.environment import ENV

from enum import Enum, unique

@unique
class Role(Enum):
    admin: int = 0
    user: int = 1
    maintainer: int = 2

class User(Base):
    _CLASS: str = "user"
    _properties: dict[str, object] = {
        "username": str,
        "first_name": str,
        "last_name": str,
        "password": str,
        "role": Role
    }

    username: str = None
    first_name: str = None
    last_name: str = None
    password: str = None
    role: Role = None

    def toDict(self) -> dict:
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "role": self.role.value,
        }

    @classmethod
    def fromDict(cls: User, data: dict) -> User | None:
        if not cls.isValid(data):
            return None
        elif len(data["password"]) > ENV.max_password_len:
            cls._logger.error(f"Password len for user {data['username']} is greater than the max length {ENV.max_password_len}.")
            return None

        model: User = User(data["username"], cls._CLASS)
        
        model.username = cls._properties["username"](data["username"])
        model.first_name = cls._properties["first_name"](data["first_name"])
        model.last_name = cls._properties["last_name"](data["last_name"])
        model.password = cls._properties["password"](data["password"])
        model.role = cls._properties["role"](data["role"])

        return model

    def isAdmin(self) -> bool:
        return self.role is Role.admin

    def isMaintainer(self) -> bool:
        return (self.role is Role.maintainer) or self.isAdmin()

    def isUser(self) -> bool:
        return (self.role is Role.user) or self.isMaintainer()
