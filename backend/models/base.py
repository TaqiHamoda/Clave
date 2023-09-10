from __future__ import annotations
from typing_extensions import Self

from models.database import Database

class Base(Database):
    # Every model needs to have a _CLASS and _properties static vars
    _CLASS: str = None
    _properties: dict[str, object] = None

    def __init__(self, key: str, classname: str) -> None:
        if not bool(classname):
            raise Exception("Can't have an empty or None classname.")
        elif not bool(key):
            raise Exception("Can't have an empty or None key.")

        super().__init__(key=key, database=classname.lower())
        
    def toDict(self) -> dict:
        """
        Transforms the model object into a dictionary representation. Returns
        True if successful, False otherwise.
        """
        raise NotImplementedError("Method has not been implemented")

    @classmethod
    def fromDict(cls: Self, data: dict) -> Self | None:
        """
        Creates a model object from the dictionary representation. Will return
        None if the dictionary is not an accurate representation.
        """
        raise NotImplementedError("Method has not been implemented")

    @classmethod
    def isValid(cls: Self, data: dict) -> bool:
        """
        Ensures that the dictionary provided is a valid representation of this
        model.
        """
        for property in cls._properties.keys():
            if data[property] is None:
                cls._logger.warning(f"Property {property} is missing in class {cls._CLASS}.")
                return False
            
            try:
                cls._properties[property](data[property])
            except Exception as e:
                cls._logger.warning(f"Property {property} is of the incorrect type {type(data[property])} in class {cls._CLASS}.")
                return False

        return True

    @classmethod
    def get(cls: Self, key: str) -> Self | None:
        """
        Gets the model data from the database. Returns None if data doesn't
        exist.
        """
        model: Self = cls(key, cls._CLASS)

        if not model.exists():
            return None

        return cls.fromDict(model._get())

    @classmethod
    def getAll(cls: Self) -> list[Self]:
        model: Self = cls(cls._CLASS, cls._CLASS)
        data: list[dict] = model._getAll()

        return [cls.fromDict(info["doc"]) for info in data]

    def update(self) -> bool:
        """
        Updates the data in the database with the data provided in this model.
        Returns True if successful, False otherwise.
        """
        return bool(self._update(data=self.toDict()))

    def exists(self) -> bool:
        """
        Checks if the object is represented in the Database.
        """
        return self._exists()

    def create(self) -> bool:
        """
        Creates an object in the database to represent the data provided to this model.
        Returns True if successful, False otherwise.
        """
        return bool(self._create(data=self.toDict()))

    def remove(self) -> bool:
        """
        Removes this object from the database. Returns True if successful,
        False otherwise.
        """
        return bool(self._remove())

    

    
