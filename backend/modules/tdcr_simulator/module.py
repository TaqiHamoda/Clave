from opencr_modules.simulator import Simulator

from typing import Callable

from time import time

class TDCRSimulator(Simulator):
    _NAME: str = "TDCR-Simulator"

    theta1: float = 0
    theta2: float = 0
    theta3: float = 0

    def recalibrate(self) -> bool:
        if self._asleep:
            return False

        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0

        return super().recalibrate()

    def getState(self) -> dict:
        state: dict = super().getState()
        state["Thetas"] = {
            "Theta Values": [self.theta1, self.theta2, self.theta3]
        }
        return state

    def run(self, experiment: dict, callback: Callable) -> dict:
        motion_func = self._run(experiment["base"])
        if motion_func is None:
            return self.getState()

        # Time keeping variables
        run_time: float = self.getRandomFloat(self.min_experiment_time, self.max_experiment_time)
        curr_time: float = time()
        t: float = time() - curr_time

        # Run the actual experiment
        err: float = self.getRandomFloat(-1, 1)
        while t < run_time:
            thetas: tuple[float] = (
                experiment["base"]["Theta 1"]*motion_func(t, run_time) + self.theta1,
                experiment["base"]["Theta 2"]*motion_func(t, run_time) + self.theta2,
                experiment["base"]["Theta 3"]*motion_func(t, run_time) + self.theta3,
            )
            report: dict = {"base": {
                "Theta 1": thetas[0] + err,
                "Theta 2": thetas[1] + err,
                "Theta 3": thetas[2] + err,
                "Expected Theta 1": thetas[0],
                "Expected Theta 2": thetas[1],
                "Expected Theta 3": thetas[2],
            }, "carriage": []}

            for info in experiment["carriage"]:
                # Carriage values at current time
                alpha: float = info["Alpha"]*motion_func(t, run_time) + self._carriages[info["_index"]].alpha
                beta: float = info["Beta"]*motion_func(t, run_time) + self._carriages[info["_index"]].beta

                report["carriage"].append({
                    "_index": info["_index"],
                    "Alpha": alpha + err,
                    "Beta": beta + err,
                    "Expected Alpha": alpha,
                    "Expected Beta": beta,
                })

            # Report values and update time
            callback(report)
            t = time() - curr_time

        # Update simulator status
        self._settings_lock.acquire()
        self.theta1 += experiment["base"]["Theta 1"] + err
        self.theta2 += experiment["base"]["Theta 2"] + err
        self.theta3 += experiment["base"]["Theta 3"] + err

        for info in experiment["carriage"]:
            self._carriages[info["_index"]].alpha += info["Alpha"] + err
            self._carriages[info["_index"]].beta += info["Beta"] + err

        self.error = ""
        self.warning = ""
        self.info = "Finished running the experiment successfully"
        self.running = False
        self.ready = True
        self.issue = False
        self._settings_lock.release()

        return self.getState()

MODULE = TDCRSimulator()