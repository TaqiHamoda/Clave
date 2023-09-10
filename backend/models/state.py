from __future__ import annotations

from models.base import Base
from models.configuration import Configuration
from engines.configuration.properties import State as EngineState

from datetime import datetime

class State(Base):
    _CLASS: str = "State"
    _properties: dict[str, object] = {
        "name": str,
        "last_update": datetime.fromisoformat,
        "state": dict,
    }

    name: str = None
    last_update: datetime = None
    state: dict = None

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "last_update": self.last_update.isoformat(),
            "state": self.state,
        }

    @classmethod
    def fromDict(cls: State, data: dict) -> State | None:
        if not cls.isValid(data):
            return None

        model: State = State(data["name"], cls._CLASS)

        model.name = cls._properties["name"](data["name"])
        model.last_update = cls._properties["last_update"](data["last_update"])
        model.state = cls._properties["state"](data["state"])

        return model

    @classmethod
    def fromModule(cls: State, name: str, state: dict) -> State | None:
        if not bool(name):
            cls._logger.error("Module name cannot be None or empty string.")
            return None

        configuration: Configuration = Configuration.get(name)
        if configuration is None:
            cls._logger.error(f"The Configuration for module {name} doesn't exist.")
            return None
        elif not EngineState.isValid(configuration.state, state):
            cls._logger.error(f"The state provided for module {name} is not valid: {state}.")
            return None

        return cls.fromDict({
            "name": name,
            "last_update": datetime.now().isoformat(),
            "state": state
        })

