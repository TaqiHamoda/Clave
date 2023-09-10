from __future__ import annotations

import os, json, logging
from typing_extensions import Self

from utilities.environment import ENV

class Cache:
    _logger: logging.Logger = logging.getLogger()
    _DIR: str = None

    @classmethod
    def _createDir(cls: Cache, dir_path: str) -> bool:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            return True

        try:
            os.mkdir(dir_path)
            return True
        except Exception as e:
            cls._logger.error("Couldn't create the caching directory.")
            cls._logger.exception(e)

            return False

    @classmethod
    def exists(cls: Cache, name: str) -> bool:
        return os.path.exists(f"{cls._DIR}/{ENV.app_name}/{name}") and os.path.isdir(f"{cls._DIR}/{ENV.app_name}")

    @classmethod
    def save(cls: Cache, name: str, data: str) -> bool:
        if not cls._createDir(f"{cls._DIR}/{ENV.app_name}"):
            return False

        try:
            with open(f"{cls._DIR}/{ENV.app_name}/{name}", mode="w") as cache_file:
                cache_file.write(data)

            return True
        except Exception as e:
            cls._logger.error(f"Couldn't save the data to cache file: {cls._DIR}/{ENV.app_name}/{name}.")
            cls._logger.exception(e)

            return False

    @classmethod
    def load(cls: Cache, name: str) -> str:
        if not cls.exists(name):
            raise Exception(f"Cache file {cls._DIR}/{ENV.app_name}/{name} doesn't exist.")

        try:
            with open(f"{cls._DIR}/{ENV.app_name}/{name}", mode="r") as cache_file:
                return cache_file.read()
        except Exception as e:
            cls._logger.error(f"Couldn't load the data from cache file: {cls._DIR}/{ENV.app_name}/{name}.")
            
            raise e

    @classmethod
    def remove(cls: Cache, name: str) -> str:
        if not cls.exists(name):
            return True

        try:
            os.remove(f"{cls._DIR}/{ENV.app_name}/{name}")
            return True
        except Exception as e:
            cls._logger.error(f"Couldn't remove the cache file: {cls._DIR}/{ENV.app_name}/{name}.")
            cls._logger.exception(e)

            return False


class FileCache(Cache):
    _DIR: str = "/tmp/"  # Use the linux tmp directory to cache files to disk


class MemoryCache(Cache):
    _DIR: str = "/dev/shm/"  # Use the linux shared memory directory to cache files to memory


class CacheObject:
    _cache_store: Cache = None

    name: str = None

    def __init__(self, name: str, cache_store: Cache) -> None:
        if not isinstance(cache_store, Cache):
            raise Exception("The cache store must be of type Cache.")
        elif self._cache_store == None:
            self.initialize(cache_store)
        
        self.name = name

    @classmethod
    def initialize(cls, cache_store: Cache) -> None:
        if not isinstance(cache_store, Cache):
            raise Exception("The cache store must be of type Cache.")

        cls._cache_store = cache_store

    def toDict(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    def fromDict(data: dict) -> Self:
        raise NotImplementedError()

    def save(self) -> bool:
        if self._cache_store is None:
            raise Exception("The Cache Object has not been initialized with a proper Cache.")
        elif self.name is None:
            raise Exception("The Cache Object has no proper name.")

        data: dict = self.toDict()
        return self._cache_store.save(self.name, json.dumps(data))

    def remove(self) -> bool:
        if self._cache_store is None:
            raise Exception("The Cache Object has not been initialized with a proper Cache.")
        elif self.name is None:
            raise Exception("The Cache Object has no proper name.")

        return self._cache_store.remove(self.name)

    @classmethod
    def exists(cls: CacheObject, name: str) -> bool:
        if cls._cache_store is None:
            raise Exception("The Cache Object has not been initialized with a proper Cache.")

        return cls._cache_store.exists(name)

    @classmethod
    def load(cls, name: str) -> Self:
        if cls._cache_store is None:
            raise Exception("The Cache Object has not been initialized with a proper Cache.")

        data: str = cls._cache_store.load(name)
        return cls.fromDict(json.loads(data))    
