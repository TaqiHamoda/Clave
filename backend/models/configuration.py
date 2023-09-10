from __future__ import annotations

from models.base import Base
from engines.configuration.properties import PROPERTIES

import json

class Configuration(Base):
    _CLASS: str = "Configuration"
    _properties: dict[str, object] = {
        "name": str,
        "description": str,
        "image": str,
        "settings": dict,
        "report": dict,
        "experiment": dict,
        "state": dict,
        "commands": dict,
    }

    name: str = None
    description: str = None
    image: str = None
    settings: dict = None
    report: dict = None
    experiment: dict = None
    state: dict = None
    commands: dict = None

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "settings": self.settings,
            "report": self.report,
            "experiment": self.experiment,
            "state": self.state,
            "commands": self.commands,
        }

    @classmethod
    def fromDict(cls: Configuration, data: dict) -> Configuration | None:
        if not cls.isValid(data):
            return None

        model: Configuration = Configuration(data["name"], cls._CLASS)

        model.name = cls._properties["name"](data["name"])
        model.description = cls._properties["description"](data["description"])
        model.image = cls._properties["image"](data["image"])
        model.settings = cls._properties["settings"](data["settings"])
        model.report = cls._properties["report"](data["report"])
        model.experiment = cls._properties["experiment"](data["experiment"])
        model.state = cls._properties["state"](data["state"])
        model.commands = cls._properties["commands"](data["commands"])

        return model

    @classmethod
    def fromFile(cls: Configuration, file_path: str) -> Configuration | None:
        configuration: dict = None
        
        with open(file_path, "r") as f:
            configuration = json.load(f)

        if configuration["name"] is None:
            cls._logger.error(f"There is no name in configuration file: {file_path}")
            return None
        elif configuration["description"] is None:
            cls._logger.error(f"There is no description in configuration file: {file_path}")
            return None
        elif configuration["image"] is None:
            cls._logger.warning(f"There is no image in configuration file: {file_path}")

        for property in PROPERTIES.keys():
            cls._logger.debug(f"Parsing the {property} for {configuration['name']}.")

            if configuration[property] is None:
                cls._logger.error(f"Property {property} is missing from {configuration['name']}")
                return None
            elif not PROPERTIES[property].isValidConfig(configuration[property]):
                return None

        return cls.fromDict(configuration)
        

