from __future__ import annotations

from models.base import Base

class ReportData(Base):
    _CLASS: str = "report_data"
    _properties: dict[str, object] = {
        "user": str,
        "experiment": str,
        "data": list,
    }

    user: str = None
    experiment: str = None
    data: list[tuple[str, dict]] = None  # The tuple is (datetime, data)

    def toDict(self) -> dict:
        return {
            "user": self.user,
            "experiment": self.experiment,
            "data": self.data
        }

    @classmethod
    def fromDict(cls: ReportData, data: dict) -> ReportData | None:
        if not cls.isValid(data):
            return None

        model: ReportData = ReportData(f'{data["user"]}-{data["experiment"]}', cls._CLASS)
        
        model.user = cls._properties["user"](data["user"])
        model.experiment = cls._properties["experiment"](data["experiment"])
        model.data = cls._properties["data"](data["data"])

        return model
