from __future__ import annotations
from datetime import datetime

from models.base import Base

class Report(Base): 
    _CLASS: str = "report"
    _properties: dict[str, object] = {
        "user": str,
        "experiment": str,
        "module": str,
        "timestamp": datetime.fromisoformat,
        "running": bool,
        "datapoints": int,
    }

    user: str = None
    experiment: str = None
    module: str = None
    timestamp: datetime = None
    running: bool = None
    datapoints: int = None

    def toDict(self) -> dict:
        return {
            "user": self.user,
            "experiment": self.experiment,
            "module": self.module,
            "timestamp": self.timestamp.isoformat(),
            "running": self.running,
            "datapoints": self.datapoints
        }

    @classmethod
    def fromDict(cls: Report, data: dict) -> Report | None:
        if not cls.isValid(data):
            return None

        model: Report = Report(f'{data["user"]}-{data["experiment"]}', cls._CLASS)
        
        model.user = cls._properties["user"](data["user"])
        model.experiment = cls._properties["experiment"](data["experiment"])
        model.module = cls._properties["module"](data["module"])
        model.timestamp = cls._properties["timestamp"](data["timestamp"])
        model.running = cls._properties["running"](data["running"])
        model.datapoints = cls._properties["datapoints"](data["datapoints"])

        return model
