import logging
from datetime import datetime
from multiprocessing.connection import Connection

from engines.module.module_messages import Commands, ModuleResponse

from models.state import State
from models.report import Report
from models.report_data import ReportData
from models.device import Device

logger: logging.Logger = logging.getLogger()

class ModuleHandlerHelper:
    @staticmethod
    def handleResponse(device_name: str, response: ModuleResponse) -> None:
        if not response.success:
            ModuleHandlerHelper.reportError(device_name, response)
            return

        try:
            if response.command in (Commands.run, Commands.execute, Commands.getState):
                state: State = State.fromModule(device_name, response.result)

                if state != None:
                    if state.exists():
                        state.update()
                    else:
                        state.create()
            elif response.command in (Commands.getSettings, Commands.changeSettings):
                device: Device = Device.get(device_name)

                if device != None:
                    device.settings = response.result

                    if device.exists():
                        device.update()
                    else:
                        device.create()
            elif response.command == Commands.getStatus:
                device: Device = Device.get(device_name)
                
                if device != None:
                    device = Device.fromDict({
                        "name": device.name,
                        "status": response.result,
                        "settings": device.settings
                    })

                    if device.exists():
                        device.update()
                    else:
                        device.create()
        except Exception as e:
            response.success = False
            response.error = f"Couldn't update device info from ModuleProcess: {e}"

            ModuleHandlerHelper.reportError(device_name, response)


    @staticmethod    
    def reportError(device_name: str, response: ModuleResponse) -> None:
        if response.success:
            return

        try:
            device: Device = Device.get(device_name)

            if device != None:
                device.status["issue"] = True
                device.status["error"] = response.error

                if device.exists():
                    device.update()
                else:
                    device.create()
        except Exception as e:
            logger.exception(e)


    @staticmethod
    def runExperiment(read_pipe: Connection, user: str, experiment: str, device_name: str) -> None:
        """
        Assumes run command has already been executed successfully.
        """
        report: Report = Report.fromDict({
            "user": user,
            "experiment": experiment,
            "module": device_name,
            "timestamp": datetime.now().isoformat(),
            "running": True,
            "datapoints": 0
        })

        if not report.exists():
            report.create()

        report_data: ReportData = ReportData.fromDict({
            "user": user,
            "experiment": experiment,
            "data": []
        })

        if not report_data.exists():
            report_data.create()

        try:
            while True:
                read_pipe.poll(timeout=None)
                data = read_pipe.recv()

                if data == 0:
                    break

                report_data.data.append((datetime.now().isoformat(), data))
                report_data.update()

                report.datapoints += 1
                report.update()
        except Exception as e:
            ModuleHandlerHelper.reportError(device_name, ModuleResponse.fromDict({
                "command": Commands.none,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "result": None,
                "error": f"Error occurred while reporting data for experiment {report.experiment}: {e}."
            }))
        finally:
            report.running = False
            report.update()
