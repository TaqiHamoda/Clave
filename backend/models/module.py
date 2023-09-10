from __future__ import annotations

from models.base import Base
from models.configuration import Configuration
from models.image import Image
from models.device import Device

from utilities.environment import ENV

import os

class Module(Base):
    _CLASS: str = "module"
    _properties: dict[str, object] = {
        "name": str,
        "image_name": str,
        "dir_name": str
    }

    name: str = None
    dir_name: str = None
    image_name: str = None

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "dir_name": self.dir_name,
            "image_name": self.image_name
        }

    @classmethod
    def fromDict(cls: Module, data: dict) -> Module | None:
        if not cls.isValid(data):
            return None

        model: Module = Module(data["name"], cls._CLASS)

        model.name = cls._properties["name"](data["name"])
        model.dir_name = cls._properties["dir_name"](data["dir_name"])
        model.image_name = cls._properties["image_name"](data["image_name"])

        return model

    @classmethod
    def loadFromDir(cls: Module, dir_name: str) -> Module | None:
        if not os.path.isdir(f"{ENV.module_path}/{dir_name}"):
            return None

        if not os.path.isfile(f"{ENV.module_path}/{dir_name}/config.json"):
            return None
        elif not os.path.isfile(f"{ENV.module_path}/{dir_name}/module.py"):
            return None

        # Parse the configuration
        configuration: Configuration = Configuration.fromFile(f"{ENV.module_path}/{dir_name}/config.json")
        if configuration is None:
            raise Exception(f"Couldn't parse the config.json at {dir_name}")

        # Save the module and the configuration to the DB
        if configuration.exists():
            configuration.update()
        else:
            configuration.create()

        module: Module = Module.fromDict({
            "name": configuration.name,
            "dir_name": dir_name,
            "image_name": configuration.image if configuration.image else ""
        })

        if module.exists():
            module.update()
        else:
            module.create()

        device: Device = Device.fromDict({
            "name": module.name,
            "status": {
                "ready": False,
                "running": False,
                "issue": True,
                "info": "",
                "warning": "",
                "error": "Device has not been initialized yet.",
                "carriages_count": 0,
            },
            "settings": {}
        })

        if device.exists():
            device.update()
        else:
            device.create()

        if configuration.image != None and os.path.isfile(f"{ENV.module_path}/{dir_name}/{configuration.image}"):
            image: Image = Image.fromFile(f"{ENV.module_path}/{dir_name}/{configuration.image}")
            if image.exists():
                image.update()
            else:
                image.create()

        return module

        
