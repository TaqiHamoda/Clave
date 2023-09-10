from __future__ import annotations
from datetime import datetime


from models.base import Base

class Experiment(Base):
    _CLASS: str = "experiment"
    _properties: dict[str, object] = {
        "name": str,
        "user": str,
        "module": str,
        "timestamp": datetime.fromisoformat,
        "parameters": dict,
    }

    name: str = None
    user: str = None
    module: str = None
    timestamp: datetime = None
    parameters: dict = None

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "user": self.user,
            "module": self.module,
            "timestamp": self.timestamp.isoformat(),
            "parameters": self.parameters,
        }

    @classmethod
    def fromDict(cls: Experiment, data: dict) -> Experiment | None:
        if not cls.isValid(data):
            return None

        model: Experiment = Experiment(f'{data["user"]}-{data["name"]}', cls._CLASS)
        
        model.name = cls._properties["name"](data["name"])
        model.user = cls._properties["user"](data["user"])
        model.module = cls._properties["module"](data["module"])
        model.timestamp = cls._properties["timestamp"](data["timestamp"])
        model.parameters = cls._properties["parameters"](data["parameters"])

        return model
