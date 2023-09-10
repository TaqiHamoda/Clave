from __future__ import annotations

from collections.abc import Iterable
import logging

from utilities.environment import ENV

class DataType:
    _logger: logging.Logger = logging.getLogger()
    
    @classmethod
    def _isValidString(cls: DataType, value: str) -> bool:
        if (value is None) or (type(value) is not str):
            return False
        elif (ENV.max_string_length > 0) and (len(value) > ENV.max_string_length):
            cls._logger.error(f"You can't have a string that is more than {ENV['max-string-size']} characters: {value}")
            return False

        return True

    @staticmethod
    def _isValidDictionary(value: dict) -> bool:
        return (value is not None) and (type(value) is dict)

    @classmethod
    def validConfig(cls: DataType, config: dict) -> bool:
        if not cls._isValidDictionary(config):
            cls._logger.error("The provided datatype configuration is not a JSON object.")
            return False
        elif config.get("type") is None:
            cls._logger.error('Every user defined property must have a "type".')
            return False
        elif not cls._isValidString(config.get("type")):
            cls._logger.error('"type" is not a valid string.')
            return False
        elif config.get("description") is None:
            cls._logger.error('Every user defined property must have a "description".')
            return False
        elif not cls._isValidString(config.get("description")):
            cls._logger.error('"description" is not a valid string.')
            return False
        elif (config.get("unit") is not None) and (not cls._isValidString(config.get("unit"))):
            cls._logger.error('"unit" is not a valid string.')
            return False
        elif (config.get("independent") is not None) and (type(config.get("independent")) is not bool):
            cls._logger.error('"independent" is not a valid boolean.')
            return False

        return True

    @staticmethod
    def validValue(value: object) -> bool:
        raise NotImplementedError()

    @classmethod
    def isValid(cls: DataType, config: dict, value: object):
        if not cls.validValue(value):
            cls._logger.error(f'The value {value} is not correct.')
            return False

        return cls.validConfig(config)


class BooleanDataType(DataType):
    @staticmethod
    def validValue(value: object) -> bool:
        return (value is not None) and (type(value) is bool)


class NumberDataType(DataType):
    @staticmethod
    def validValue(value: object) -> bool:
        return (value is not None) and ((type(value) is float) or (type(value) is int))

    @classmethod
    def validConfig(cls: DataType, config: dict) -> bool:
        if not super().validConfig(config):
            return False
        elif (config.get("min") is not None) and (not cls.validValue(config.get("min"))):
            cls._logger.error(f'Property "min" is not valid: {config.get("min")}.')
            return False
        elif (config.get("max") is not None) and (not cls.validValue(config.get("max"))):
            cls._logger.error(f'Property "max" is not valid: {config.get("max")}.')
            return False
        elif (config.get("min") is not None) and (config.get("max") is not None) and (config.get("min") > config.get("max")):
            cls._logger.error(f'Property "min" must be less than or equal to property "max". min: {config.get("min")}, max: {config.get("max")}')
            return False
        elif (config.get("step") is not None) and (not cls.validValue(config.get("step"))):
            cls._logger.error(f'Property "step" is not valid: {config.get("step")}.')
            return False
        elif config.get("unit") is None:
            cls._logger.warning('It is strongly recommended to add a unit.')
        elif not cls._isValidString(config.get("unit")):
            return False
        
        return True
        

class IntegerDataType(NumberDataType):
    @staticmethod
    def validValue(value: object) -> bool:
        return (value is not None) and (type(value) is int)


class TextDataType(DataType):
    @staticmethod
    def validValue(value: object) -> bool:
        return DataType._isValidString(value)


class ListDataType(DataType):
    _TYPES: dict[str, DataType] = {
        "boolean": BooleanDataType,
        "number": NumberDataType,
        "integer": IntegerDataType,
        "text": TextDataType,
    }

    @staticmethod
    def validValue(value: object) -> bool:
        return (value is not None) and isinstance(value, Iterable)

    @classmethod
    def validConfig(cls: DataType, config: dict) -> bool:
        if not super().validConfig(config):
            return False
        elif config.get("value") is None:
            cls._logger.error('A list must have a "value" property.')
            return False
        elif cls._TYPES[config.get("value")] is None:
            cls._logger.error(f'"value" must have a valid type. Type {config.get("value")} is unknown.')
            return False

        return True

    @classmethod
    def isValid(cls: DataType, config: dict, value: object):
        if not super().isValid(config, value):
            return False

        for data in value:
            if not cls._TYPES[config.get("value")].isValid(config, data):
                cls._logger.error(f'{value} is not of type "{config.get("value")}".')
                return False

        return True


class EnumerationDataType(ListDataType):
    @classmethod
    def validConfig(cls: DataType, config: dict) -> bool:
        if not super().validConfig(config):
            return False
        elif (config.get("values") is None) or (not cls.validValue(config.get("values"))):
            cls._logger.error('An enumeration must have a proper "values" property.')
            return False
        elif not BooleanDataType.validValue(config.get("multiple")):
            cls._logger.error('An enumeration must have a "multiple" property that is a boolean.')
            return False

        return True

    @classmethod
    def isValid(cls: DataType, config: dict, value: object):
        if not super().isValid(config, value):
            return False
        elif (not config.get("multiple")) and (len(value) > 1):
            cls._logger.error(f'Only a single value can be chosen.')
            return False

        for data in value:
            if data not in config.get("values"):
                cls._logger.error(f'The value provided {data} is not in the values list: {config.get("values")}.')
                return False

        return True


DATA_TYPES: dict[str, DataType] = {
    "boolean": BooleanDataType,
    "number": NumberDataType,
    "integer": IntegerDataType,
    "text": TextDataType,
    "list": ListDataType,
    "enumeration": EnumerationDataType,
}