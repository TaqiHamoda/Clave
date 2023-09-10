from opencr_modules.device import Device

from random import random
from threading import Timer, Lock
from time import sleep, time
import math
import logging
from typing import Callable

class Carriage:
    alpha: float = 0
    beta: float = 0

class _Simulator(Device):
    _logger: logging.Logger = None

    # Sleep Properties
    duration: int = 5
    frequency: int = 60
    sleeper: Timer = None
    _asleep: bool = False
    will_sleep: bool = False
    _sleep_lock: Lock = Lock()

    def __init__(self, device_name: str) -> None:
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S %p",
            level=logging.DEBUG,
            filemode="a"
        )

        self._logger = logging.getLogger(device_name)

        self.ready = True
        self.info = "Device is ready and awaiting instructions."

    def _wakeup(self) -> None:
        self._sleep_lock.acquire()
        self._asleep = False
        self._sleep_lock.release()

        if self.sleeper is not None:
            self._sleep_lock.acquire()
            self.sleeper.cancel()
            self.sleeper = None
            self._sleep_lock.release()

    def wakeup(self) -> None:
        self._wakeup()

        self._sleep_lock.acquire()
        self._asleep = False
        self._sleep_lock.release()

    def _sleep(self, frequency: int, duration: int) -> None:
        if self.sleeper is None:
            self._sleep_lock.acquire()
            self._asleep = False
            self._sleep_lock.release()

            return None

        while self.will_sleep:
            self._sleep_lock.acquire()
            self._asleep = True
            self._sleep_lock.release()

            sleep(duration)

            self._sleep_lock.acquire()
            self._asleep = False
            self._sleep_lock.release()

            if frequency <= 0:
                break

            sleep(frequency)

        self._wakeup()

    def goAsleep(self, frequency: int, duration: int) -> None:
        if self._asleep:
            return None
        elif (duration <= 0) or (frequency <= 0):
            self.wakeup()
            return None

        self._sleep_lock.acquire()
        self.will_sleep = True
        self.duration = duration
        self.frequency = frequency
        self.sleeper = Timer(self.duration, self._sleep, (frequency, duration))
        self._sleep_lock.release()

    # Motion Profile Methods
    @staticmethod
    def third_order_polynomial(t: float, T: float) -> float:
        # Assumes s(0) = s'(0) = s'(T) = 0 and s(T) = 1
        return 3*math.pow(t/T, 2) - 2*math.pow(t/T, 3)

    @staticmethod
    def fifth_order_polynomial(t: float, T: float) -> float:
        # Assumes s(0) = s'(0) = s'(T) = s''(0) = s''(T) = 0 and s(T) = 1
        return 10*math.pow(t/T, 3) - 15*math.pow(t/T, 4) + 6*math.pow(t/T, 5)

class Simulator(_Simulator):
    _NAME: str = None

    # Simulator Settings
    carriages_count: int = 3
    min_experiment_time: int = 600
    max_experiment_time: int = 900
    probability_failure: float = 10

    # Error and Warning Settings
    error_period: int = 3600
    warning_period: int = 1800
    _error_timer: Timer = None
    _warning_timer: Timer = None

    # Simulator Specific Values
    _carriages: list[Carriage] = [Carriage() for _ in range(carriages_count)]
    _max_len: int = 100
    _max_speed: int = 255
    _carriage_len: int = 10

    # Locks
    _run_lock: Lock = Lock()
    _settings_lock: Lock = Lock()

    def __init__(self) -> None:
        super().__init__(self._NAME)
        
        if self._error_timer is not None:
            self._error_timer.cancel()

        if self._warning_timer is not None:
            self._warning_timer.cancel()

        self._error_timer = Timer(self.error_period, self._error, None)
        self._warn_timer = Timer(self.warning_period, self._warn, None)


    def _warn(self) -> None:
        while self.warning_period > 0:
            sleep(self.warning_period)

            self._settings_lock.acquire()
            self.warning = "This is the repeating warning message."
            self._settings_lock.release()

    def _error(self) -> None:
        while self.error_period > 0:
            sleep(self.error_period)

            self._settings_lock.acquire()
            self.error = "This is the repeating error message."
            self._settings_lock.release()

    @staticmethod
    def getRandomFloat(min: float, max: float) -> float:
        if min > max:
            raise Exception("The min cannot be greater than max.")

        # r*max + (1 - r)*min = r*max + min - r*min = r*(max - min) + min
        return random()*(max - min) + min

    def getState(self) -> dict:
        if self._asleep:
            return {}

        return {
            "Sleep Status": {
                "Will Sleep": self.will_sleep,
                "Duration": self.duration,
                "Frequency": self.frequency,
            },
            "Carriages": {
                "Alpha Values": [c.alpha for c in self._carriages],
                "Beta Values": [c.beta for c in self._carriages]
            }
        }

    def getSettings(self) -> dict:
        if self._asleep:
            return {}

        return {
            "Experiment Settings": {
                "Max Experiment Run-Time": self.max_experiment_time,
                "Probability of Failure": self.probability_failure,
            },
            "Simulator Settings": {
                "Error Period": self.error_period,
                "Warning Period": self.warning_period,
                "Number of Carriages": self.carriages_count
            }
        }

    def changeSettings(self, settings: dict) -> dict:
        if self._asleep:
            return False

        # I assume values provided are correct for my sake
        _settings: dict = {
            "Experiment Settings": {
                "Max Experiment Run-Time": int,
                "Probability of Failure": float,
            },
            "Simulator Settings": {
                "Error Period": int,
                "Warning Period": int,
                "Number of Carriages": int
            }
        }
        
        # I will just do basic error checking
        for configSettings in _settings.keys():
            for setting in _settings[configSettings].keys():
                if settings[configSettings][setting] is None:
                    raise Exception(f"{setting} is expected to be provided.")

                try:
                    _settings[configSettings][setting](settings[configSettings][setting])
                except Exception as e:
                    raise Exception(f"{setting} is expected to be of type {_settings[configSettings][setting]}")

        self._settings_lock.acquire()
        self.max_experiment_time = int(settings["Experiment Settings"]["Max Experiment Run-Time"])
        self.probability_failure = float(settings["Experiment Settings"]["Probability of Failure"])
        self.error_period = int(settings["Simulator Settings"]["Error Period"])
        self.warning_period = int(settings["Simulator Settings"]["Warning Period"])
        self.carriages_count = int(settings["Simulator Settings"]["Number of Carriages"])
        self._settings_lock.release()

        return self.getSettings()

    def stop(self) -> bool:
        if self._asleep:
            return False

        self._run_lock.acquire()
        self.running = False
        self._run_lock.release()

        return True

    def recalibrate(self) -> bool:
        if self._asleep:
            return False

        try:
            self._carriages = [Carriage() for _ in range(self.carriages_count)]

            self.error = ""
            self.warning = ""
            self.issue = False
            return True
        except Exception as e:
            self.error += "\n\n" + str(e)
            self.issue = True
            return False

    def reset(self) -> bool:
        if self._asleep:
            return False

        self = self.__init__()
        return True

    def reboot(self) -> bool:
        if self._asleep:
            return False

        sleep(5)
        self.wakeup()
        return True

    def poweroff(self) -> bool:
        if self._asleep:
            return False

        # Basically sleep and wakeup for an extremely short period
        self.goAsleep(1, 60)
        return True

    def execute(self, command: str, parameters: dict) -> dict:
        if self._asleep:
            return self.getState()

        if command == "Move Carriages to End":
            self.run({
                "base": {
                    "Recalibrate Beforehand": False,
                    "Motion Profile": "Third Order Polynomial",
                },
                "carriage": [
                    {
                        "_index": i,
                        "Alpha": self._carriages[i].alpha,
                        "Beta": self._max_len - i*self._carriage_len,
                    } for i in range(self.carriages_count)
                ]
            }, lambda x: None)
        elif command == "Sleep":
            if (parameters["Duration"] is None) or (parameters["Frequency"] is None):
                raise Exception("Both frequency and duration are expected to be provided.")
            elif (parameters["Duration"] is not int) or (parameters["Frequency"] is not int):
                raise Exception("Both frequency and duration are expected to be integers.")

            self.goAsleep(parameters["Frequency"], parameters["Duration"])
        elif command == "Wake-Up":
            self.wakeup()
        else:
            raise Exception(f"Command {command} is unknown.")

        return self.getState()

    def _run(self, experiment: dict) -> Callable:
        # Basically the setup to run before running the experiment
        if self._asleep:
            return None

        if self.getRandomFloat(0, 100) < self.probability_failure:
            self._settings_lock.acquire()
            self.error = "Experiment Failed"
            self.running = False
            self.ready = False
            self.issue = True
            self._settings_lock.release()

            return None

        self._settings_lock.acquire()
        self.error = ""
        self.warning = "Currently running an experiment"
        self.running = True
        self.ready = False
        self.issue = False
        self._settings_lock.release()

        # Take care of base attributes in experiment
        motion_func: function = None
        if experiment["Motion Profile"] == "Third Order Polynomial":
            motion_func = self.third_order_polynomial
        elif experiment["Motion Profile"] == "Fifth Order Polynomial":
            motion_func = self.fifth_order_polynomial
        else:
            raise Exception(f'The motion function {experiment["Motion Profile"]} is unknown.')

        if experiment["Recalibrate Beforehand"]:
            self.recalibrate()

        return motion_func

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
            report: dict = {"base": {}, "carriage": []}

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
