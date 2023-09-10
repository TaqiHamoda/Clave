from typing import Callable

# TODO: Add the connect method that recieves a dictionary and returns a list of device states

class Device:
    # Device boolean statuses
    ready: bool = False
    running: bool = False
    issue: bool = False

    # Device message statuses
    info: str = ""
    warning: str = ""
    error: str = ""

    # Device properties
    carriages_count: int = 0

    def run(self, experiment: dict, callback: Callable) -> dict:
        """
        Run the provided experiment. There is no guarantee that the dict
        provided is of the correct format.

        The callback is used to report back the data in real-time as the
        experiment is being run. The callback expects a dictionary in the
        same format as the "report" function found in the device's
        configuration. The callback is not expected to return anything.

        Returns the device state if successful. An error is expected to be
        raised for otherwise.
        """
        self.error = "Method not implemented."
        raise NotImplementedError()

    def stop(self) -> bool:
        """
        Stop any and all running experiments.

        Returns True if successful, False if otherwise. The device
        status is expected to be updated after this method is called.
        """
        self.error = "Method not implemented."
        raise NotImplementedError()

    def execute(self, command: str, parameters: dict) -> dict:
        """
        Run the provided command using the provided parameters. There is
        no guarantee that the parameters provided is of the correct
        format and there is no guarantee that the command is correct.

        Returns the device state if successful. An error is expected to be
        raised for otherwise.
        """
        self.error = "Method not implemented."
        raise NotImplementedError()

    def getState(self) -> dict:
        """
        Get the device state including the status and other device
        relevant data.

        Returns the device state if successful. An error is expected to be
        raised for otherwise.
        """
        self.error = "Method not implemented."
        raise NotImplementedError()

    def getSettings(self) -> dict:
        """
        Get the current device settings values.

        Returns the device settings if successful. An error is expected
        to be raised for otherwise.
        """
        self.error = "Method not implemented."
        raise NotImplementedError()

    def changeSettings(self, settings: dict) -> dict:
        """
        Change the device's settings to the provided settings. There
        is no guarantee that the dict provided is of the correct format.

        Returns the device settings if successful. An error is expected
        to be raised for otherwise. The device status and settings are
        expected to be updated after this method is called.
        """
        self.error = "Method not implemented."
        raise NotImplementedError()

    def getStatus(self) -> dict:
        """
        Get the device's status. This method is already provided and
        should not be changed. If changed, there is no guarantee that
        Open-CR will work correctly with the device.

        This method will not be called directly by Open-CR but rather
        should be called by the getState method.
        """
        return {
            "ready": self.ready,
            "running": self.running,
            "issue": self.issue,
            "info": self.info,
            "warning": self.warning,
            "error": self.error,
            "carriages_count": self.carriages_count
        }
