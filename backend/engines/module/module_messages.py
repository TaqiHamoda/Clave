from __future__ import annotations

import enum
from datetime import datetime

class Commands(enum.Enum):
    none: str = "none"
    run: str = "run"
    stop: str = "stop"
    execute: str = "execute"
    getState: str = "getState"
    getStatus: str = "getStatus"
    getSettings: str = "getSettings"
    changeSettings: str = "changeSettings"


class ModuleRequest:
    username: str = None
    report: str = None
    module: str = None
    command: Commands = None
    parameters: tuple = None

    @classmethod
    def fromDict(cls: ModuleRequest, data: dict) -> ModuleRequest:
        model: ModuleRequest = cls()

        model.username = data["username"]
        model.report = data["report"]
        model.module = data["module"]
        model.command = Commands(data["command"])
        model.parameters = data["parameters"]

        return model

    def toDict(self) -> dict:
        return {
            "username": self.username,
            "report": self.report,
            "module": self.module,
            "command": self.command.value,
            "parameters": self.parameters
        }


class ModuleResponse:
    command: Commands = None
    timestamp: datetime = None
    success: bool = None
    result: dict = None
    error: str = None    

    @classmethod
    def fromDict(cls: ModuleResponse, data: dict) -> ModuleResponse:
        model: ModuleResponse = cls()
        
        model.command = Commands(data["command"])
        model.timestamp = datetime.fromisoformat(data["timestamp"])
        model.success = data["success"]
        model.result = data["result"]
        model.error = data["error"]

        return model

    def toDict(self) -> dict:
        return {
            "command": self.command.value,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "result": self.result,
            "error": self.error
        }
