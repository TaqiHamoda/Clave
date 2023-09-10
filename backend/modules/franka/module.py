from opencr_modules.device import Device

from typing import Callable

from time import time, sleep
import math

class FrankaSimulator(Device):
    _NAME: str = "Franka Emika"

    actuators: list[float] = [0 for _ in range(7)]

    def __init__(self) -> None:
        super().__init__()

        # Device boolean statuses
        self.ready = True
        self.running = False
        self.issue = False

        # Device message statuses
        self.info = "Your wish is my command, Researcher!"
        self.warning = ""
        self.error = ""

    # Motion Profile Methods
    @staticmethod
    def third_order_polynomial(t: float, T: float) -> float:
        # Assumes s(0) = s'(0) = s'(T) = 0 and s(T) = 1
        return 3*math.pow(t/T, 2) - 2*math.pow(t/T, 3)

    def getState(self) -> dict:
        return {}

    def stop(self) -> bool:
        self.error = "Can't stop."
        self.issue = True
        raise False

    def execute(self, command: str, parameters: dict) -> dict:
        return {}

    def getSettings(self) -> dict:
        return {}

    def changeSettings(self, settings: dict) -> dict:
        return {}

    def run(self, experiment: dict, callback: Callable) -> dict:
        # Update simulator status
        self.error = ""
        self.warning = "Currently running an experiment"
        self.info = ""
        self.running = True
        self.ready = False
        self.issue = False

        # Time keeping variables
        run_time: float = experiment["base"]["Experiment Runtime"]
        curr_time: float = time()
        t: float = time() - curr_time

        # Run the actual experiment
        temp: list[float] = None
        while t < run_time:
            temp = [ experiment["base"][f"Actuator {i + 1}"]*self.third_order_polynomial(t, run_time) + self.actuators[i] for i in range(len(self.actuators)) ]
                
            report: dict = {"base": {
                "Time": t,
                "Actuator 1": temp[0],
                "Actuator 2": temp[1],
                "Actuator 3": temp[2],
                "Actuator 4": temp[3],
                "Actuator 5": temp[4],
                "Actuator 6": temp[5],
                "Actuator 7": temp[6],
            }, "carriage": []}

            # Report values and update time
            callback(report)
            sleep(1)
            t = time() - curr_time

        self.actuators = temp

        # Update simulator status
        self.error = ""
        self.warning = ""
        self.info = "Finished running the experiment successfully"
        self.running = False
        self.ready = True
        self.issue = False

        return self.getState()

MODULE = FrankaSimulator()