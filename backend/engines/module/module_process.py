from __future__ import annotations
from datetime import datetime

from multiprocessing.connection import Connection

from typing import Callable
import threading, logging, importlib.util

from importlib import __import__
from types import ModuleType
from importlib.machinery import ModuleSpec
from opencr_modules.device import Device

from utilities.environment import ENV
from engines.module.module_messages import Commands, ModuleRequest, ModuleResponse

class ModuleProcess:
    _logger: logging.Logger = logging.getLogger()

    _report_pipe: tuple[Connection] = None  # Used for real-time reporting of data
    _request_pipe: tuple[Connection] = None  # Used for recieving ModuleRequests
    _response_pipe: tuple[Connection] = None  # Used for sending ModuleResponses

    _commands: dict[Commands, Callable] = None

    def __init__(self, dir_name: str, report_pipe: tuple[Connection], request_pipe: tuple[Connection], response_pipe: tuple[Connection]) -> None:
        self._report_pipe = report_pipe
        self._request_pipe = request_pipe
        self._response_pipe = response_pipe

        # TODO: Make sure to enable it for production use
        # module_user_info: pwd.struct_passwd = pwd.getpwnam(ENV.module_user)
        # os.setgid(module_user_info.pw_gid)
        # os.setuid(module_user_info.pw_uid)

        # Load the module code
        spec: ModuleSpec = importlib.util.spec_from_file_location("module", f"{ENV.module_path}/{dir_name}/module.py")
        python_module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(python_module)

        device: Device = python_module.MODULE

        self._commands: dict[Commands, Callable] = {
            Commands.run: device.run,
            Commands.stop: device.stop,
            Commands.execute: device.execute,
            Commands.getState: device.getState,
            Commands.getStatus: device.getStatus,
            Commands.getSettings: device.getSettings,
            Commands.changeSettings: device.changeSettings,
        }

    def _execute(self, command: Commands, args: tuple) -> None:
        result: ModuleResponse = ModuleResponse()
        result.command = command

        try:
            try:
                result.result = self._commands[command](*args)
                result.success = True
            except Exception as e:
                self._logger.exception(e)
                result.error = str(e)
                result.success = False

            result.timestamp = datetime.now()

            if command == Commands.run:
                self._report_pipe[1].send(0)  # Send zero to indicate end of reporting

            self._response_pipe[1].send(result.toDict())
        except Exception as e:
            self._logger.exception(e)
            self._response_pipe[1].send(ModuleResponse.fromDict({
                "command": Commands.none,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "result": None,
                "error": f"Error occurred: {e}."
            }))

    def run(self) -> None:
        while True:
            try:
                if not self._request_pipe[0].poll(timeout=None):
                    self._logger.warn("Polling is unsuccessful in ModuleProcess")
                    continue

                request: ModuleRequest = ModuleRequest.fromDict(self._request_pipe[0].recv())

                if request.command == Commands.run:
                    request.parameters = (request.parameters[0], self._report_pipe[1].send)

                # Run it as a thread so it doesn't block the other requests from running
                threading.Thread(target=self._execute, args=(request.command, request.parameters)).start()
            except Exception as e:
                self._logger.exception(e)