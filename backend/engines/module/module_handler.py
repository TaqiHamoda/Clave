from __future__ import annotations
from datetime import datetime

import os, logging, threading
from multiprocessing import Process
from multiprocessing.connection import Connection, Pipe

from utilities.environment import ENV
from engines.module.module_messages import ModuleRequest, ModuleResponse, Commands
from engines.module.module_info import ModuleInfo
from engines.module.module_process import ModuleProcess
from engines.module.module_handler_helper import ModuleHandlerHelper


class ModuleHandler:
    _logger: logging.Logger = logging.getLogger()

    _module_info: ModuleInfo = None

    _report_pipe: tuple[Connection] = None
    _request_pipe: tuple[Connection] = None
    _response_pipe: tuple[Connection] = None

    def __init__(self, module_info: ModuleInfo) -> None:
        self._module_info = module_info


    @staticmethod
    def execute(request: ModuleRequest, module_info: ModuleInfo) -> ModuleResponse:
        try:
            connection: Connection = module_info.getWriteRequest()
            connection.send(request.toDict())
            connection.close()

            connection = module_info.getReadResponse()

            response: ModuleResponse = None
            if connection.poll(timeout=ENV.max_wait_runtime):
                response = ModuleResponse.fromDict(connection.recv())
            else:
                response = ModuleResponse.fromDict({
                    "command": request.command,
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "result": "",
                    "error": "Timeout occured while waiting for device to reply."
                })

            connection.close()
            return response
        except Exception as e:
            return ModuleResponse.fromDict({
                    "command": request.command,
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "result": "",
                    "error": f"An error occurred when trying to communicate with module: {e}"
                })

    def _handleReponse(self) -> None:
        while True:
            try:
                if not self._response_pipe[0].poll(timeout=None):
                    self._logger.warn("Polling is unsuccessful in ModuleHandler Handle Reponse")
                    continue

                message: dict = self._response_pipe[0].recv()
                module_response: ModuleResponse = ModuleResponse.fromDict(message)

                ModuleHandlerHelper.handleResponse(self._module_info.name, module_response)
            except EOFError as e:  # TODO: Handle the eof error if it pops up
                self._logger.exception(e)
                print(f"EOFError ModuleHandler _handle_response: {e}")
            except Exception as e:
                self._logger.exception(e)

    def _run(self) -> None:
        while True:
            try:
                # Block indefintely until pipe is ready for reading
                connection: Connection = self._module_info.getReadRequest()

                if not connection.poll(timeout=None):
                    self._logger.warn("Poll is unsuccessful in ModuleHandler run")
                    continue

                message: dict = connection.recv()
                connection.close()

                module_request: ModuleRequest = ModuleRequest.fromDict(message)

                # Send request to the ModuleProcess for processing
                self._request_pipe[1].send(module_request.toDict())

                if module_request.command == Commands.run:
                    Process(target=ModuleHandlerHelper.runExperiment, args=(
                        self._report_pipe[0],
                        module_request.username,
                        module_request.report,
                        module_request.module
                    )).start()

                connection = self._module_info.getWriteResponse()
                connection.send(ModuleResponse.fromDict({
                    "command": module_request.command,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "result": None,
                    "error": None
                }).toDict())
                connection.close()
            except EOFError as e:
                self._logger.exception(e)
                self._module_info.recreatePipes()
            except Exception as e:
                self._logger.exception(e)


    def run(self, module_dir_name: str) -> None:
        """
        Runs the ModuleHandler in a seperate process.
        
        Returns the pid if successful
        """
        handler_pid: int = os.fork()

        if handler_pid < 0:
            raise Exception("Couldn't create a process for ModuleHandler")
        elif handler_pid > 0:  # Parent Process
            self._module_info.handler_pid = handler_pid
            self._module_info.save()
            return

        self._report_pipe = Pipe()
        self._request_pipe = Pipe()
        self._response_pipe = Pipe()

        process_pid: int = os.fork()
        
        if process_pid < 0:
            raise Exception("Couldn't create a process for ModuleProcess")
        elif process_pid == 0:  # Child Process
            module_process: ModuleProcess = ModuleProcess(module_dir_name, self._report_pipe, self._request_pipe, self._response_pipe)
            module_process.run()

        self._module_info = ModuleInfo.load(self._module_info.name)
        self._module_info.process_pid = process_pid
        self._module_info.save()

        threading.Thread(target=self._handleReponse, args=()).start()
        self._run()



        
