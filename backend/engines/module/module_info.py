from __future__ import annotations

from multiprocessing.connection import Connection
import os, posix, signal, logging

from utilities.cache import MemoryCache, CacheObject
from utilities.environment import ENV

class ModuleInfo(CacheObject):
    _logger: logging.Logger = logging.getLogger()

    _request_pipe_path: str = None
    _response_pipe_path: str = None
    
    handler_pid: int = None
    process_pid: int = None

    def __init__(self, name: str) -> None:
        super().__init__(name, MemoryCache())

        if not os.path.isdir(os.path.dirname(ENV.module_handler_pipe_path)):
            os.mkdir(os.path.dirname(ENV.module_handler_pipe_path))

        self._request_pipe_path = f"{ENV.module_handler_pipe_path}/{self.name}_request"
        self._response_pipe_path = f"{ENV.module_handler_pipe_path}/{self.name}_response"

        if not os.path.exists(self._request_pipe_path):
            os.mkfifo(self._request_pipe_path)

        if not os.path.exists(self._response_pipe_path):
            os.mkfifo(self._response_pipe_path)

    def getReadRequest(self) -> Connection:
        return Connection(posix.open(self._request_pipe_path, posix.O_RDONLY | posix.O_NONBLOCK))

    def getWriteRequest(self) -> Connection:
        return Connection(posix.open(self._request_pipe_path, posix.O_WRONLY | posix.O_NONBLOCK))

    def getReadResponse(self) -> Connection:
        return Connection(posix.open(self._response_pipe_path, posix.O_RDONLY | posix.O_NONBLOCK))

    def getWriteResponse(self) -> Connection:
        return Connection(posix.open(self._response_pipe_path, posix.O_WRONLY | posix.O_NONBLOCK))

    def recreatePipes(self) -> None:
        if os.path.exists(self._request_pipe_path):
            os.remove(self._request_pipe_path)

        if os.path.exists(self._response_pipe_path):
            os.remove(self._response_pipe_path)

        os.mkfifo(self._request_pipe_path)
        os.mkfifo(self._response_pipe_path)

    @classmethod
    def initialize(cls):
        return super().initialize(MemoryCache())

    def kill(self) -> bool:
        if not self.exists(self.name):
            return True

        ret: bool = True

        try:
            if self.handler_pid != None:
                os.kill(self.handler_pid, signal.SIGTERM)
                self.handler_pid = None                
        except Exception as e:
            self._logger.error(f"Failed to kill ModuleHandler {self.name} with pid {self.handler_pid}")
            self._logger.exception(e)

            ret = False

        try:
            if self.process_pid != None:
                os.kill(self.process_pid, signal.SIGTERM)
                self.process_pid = None
        except Exception as e:
            self._logger.error(f"Failed to kill ModuleProcess {self.name} with pid {self.process_pid}")
            self._logger.exception(e)

            ret = False

        if not ret:
            return False
        elif not self.save():
            self._logger.error(f"Could not save updated ModuleProcess info after it was killed: {self.toDict()}.")
            return False

        return True

    def dispose(self) -> bool:
        try:
            if not self.exists(self.name):
                return False
            elif (not self.kill()) or (not self.remove()):
                return False

            # Remove the named pipe folders
            if os.path.exists(self._request_pipe_path):
                os.remove(self._request_pipe_path)

            if os.path.exists(self._response_pipe_path):
                os.remove(self._response_pipe_path)

            return True
        except Exception as e:
            self._logger.error(f"Couldn't dispose of the ModuleProcess {self.name}.")
            self._logger.exception(e)

            return False

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "handler_pid": self.handler_pid,
            "process_pid": self.process_pid
        }

    @classmethod
    def fromDict(cls: ModuleInfo, data: dict) -> ModuleInfo:
        model: ModuleInfo = cls(data["name"])
        model.handler_pid = data["handler_pid"]
        model.process_pid = data["process_pid"]

        return model