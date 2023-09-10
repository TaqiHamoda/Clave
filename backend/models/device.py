from __future__ import annotations

from models.base import Base

class Device(Base):
    _CLASS: str = "device"
    _properties: dict[str, object] = {
        "name": str,
        "status": dict,
        "settings": dict
    }

    name: str = None
    status: dict = None
    settings: dict = None

    @classmethod
    def _validateStatus(cls, status: dict) -> bool:
        if status == None:
            return False

        properties: dict[str, object] = {
            "ready": bool,
            "running": bool,
            "issue": bool,
            "info": str,
            "warning": str,
            "error": str,
            "carriages_count": int,
        }

        for property in properties.keys():
            if status[property] is None:
                cls._logger.warning(f"Property {property} is missing in class {cls._CLASS}.")
                return False
            
            try:
                properties[property](status[property])
            except Exception as e:
                cls._logger.warning(f"Property {property} is of the incorrect type {type(status[property])} in class {cls._CLASS}.")
                return False

        return True

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "settings": self.settings
        }

    @classmethod
    def fromDict(cls: Device, data: dict) -> Device | None:
        if not (cls.isValid(data) and cls._validateStatus(data.get("status"))):
            return None

        model: Device = Device(data["name"], cls._CLASS)

        model.name = cls._properties["name"](data["name"])
        model.status = cls._properties["status"](data["status"])
        model.settings = cls._properties["settings"](data["settings"])

        return model
