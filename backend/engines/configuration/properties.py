from __future__ import annotations

from engines.configuration.datatypes import DATA_TYPES, DataType, ListDataType

import logging

# TODO: Device ID support in state

class _Property:
    """
    This class parses and validates the individual attributes inside a property.
    """

    _logger: logging.Logger = logging.getLogger()

    @classmethod
    def isValidConfig(cls: _Property, config: dict) -> bool:
        if config is None:
            cls._logger.error(f"You cannot have a null config.")
            return False
        elif not DataType._isValidDictionary(config):
            cls._logger.error(f"You cannot have an invalid config.")
            return False

        for key in config.keys():
            cls._logger.debug(f"Parsing attribute {key}.")

            if DATA_TYPES[config[key]["type"]] is None:
                cls._logger.error(f'The type {config[key]["type"]} is unsupported.')
                return False
            elif not DATA_TYPES[config[key]["type"]].validConfig(config[key]):
                return False

        return True

    @classmethod
    def isValid(cls: _Property, config: dict, value: dict) -> bool:
        if (config is None) or (value is None):
            cls._logger.error(f"You cannot have a null config or value.")
            return False
        elif (not DataType._isValidDictionary(config)) or (not DataType._isValidDictionary(value)):
            cls._logger.error(f"You cannot have an invalid config or value.")
            return False

        for key in config.keys():
            cls._logger.debug(f"Validating attribute {key}.")

            if value[key] is None:
                cls._logger.error(f"There is no value provided for {key}.")
                return False
            elif DATA_TYPES[config[key]["type"]] is None:
                cls._logger.error(f'The type {config[key]["type"]} is unsupported.')
                return False
            elif not DATA_TYPES[config[key]["type"]].isValid(config[key], value[key]):
                return False

        return True


class Property(_Property):
    """
    This class parses the properties inside an object.
    """
    
    @classmethod
    def isValidConfig(cls: Property, config: dict) -> bool:
        for key in config.keys():
            cls._logger.debug(f"Parsing property {key}.")

            if not super().isValidConfig(config[key]):
                return False

        return True

    @classmethod
    def isValid(cls: Property, config: dict, value: dict) -> bool:
        for key in config.keys():
            cls._logger.debug(f"Validating property {key}.")

            if not DataType._isValidDictionary(value[key]):
                cls._logger.error(f"The property {key} is found in the configuration but is not provided.")
                return False
            elif not super().isValid(config[key], value[key]):
                return False

        return True


class State(Property):
    pass


class Settings(Property):
    pass


class Commands(Property):
    pass


class Experiment(Property):
    @classmethod
    def isValidConfig(cls: Experiment, config: dict) -> bool:
        if config["base"] is None:
            cls._logger.error("The base object must be defined.")
            return False
        elif config["carriage"] is None:
            cls._logger.error("The carriage object must be defined.")
            return False

        return super().isValidConfig(config)

    @classmethod
    def isValid(cls: Experiment, config: dict, value: dict) -> bool:
        if config["base"] is None:
            cls._logger.error("The base object must be defined.")
            return False
        elif config["carriage"] is None:
            cls._logger.error("The carriage object must be defined.")
            return False
        elif not ListDataType.validValue(value["carriage"]):
            cls._logger.error("The carriage value is expected to be a list of objects.")
            return False

        for carriage in value["carriage"]:
            if not _Property.isValid(config["carriage"], carriage):
                return False

        return _Property.isValid(config["base"], value["base"])


class Report(Experiment):
    pass


PROPERTIES: dict[str, Property] = {
    "state": State,
    "settings": Settings,
    "report": Report,
    "experiment": Experiment,
    "commands": Commands,
}
