from utilities.couchdb import CouchDB

import logging

# TODO: Create a get by property method so that you can get the data
# using different properties not only the key
class Database:
    _key: str = None
    _database: str = None
    
    _logger: logging.Logger = logging.getLogger()

    def __init__(self, key: str, database: str) -> None:
        self._key = key
        self._database = database

        try:
            if not CouchDB.isDatabase(database=self._database):
                CouchDB.createDatabase(database=self._database)
        except Exception as e:
            self._logger.error(e)

    def _exists(self) -> bool:
        try:
            return CouchDB.isDocument(database=self._database, document=self._key)
        except Exception as e:
            self._logger.error(e)
            return False

    def _get(self) -> dict:
        try:
            return CouchDB.getDocument(database=self._database, document=self._key)
        except Exception as e:
            self._logger.error(e)
            return {}

    def _create(self, data: dict) -> dict:
        try:
            return CouchDB.createDocument(database=self._database, document=self._key, data=data)
        except Exception as e:
            self._logger.error(e)
            return {}

    def _update(self, data: dict) -> dict:
        try:
            return CouchDB.updateDocument(database=self._database, document=self._key, data=data)
        except Exception as e:
            self._logger.error(e)
            return {}

    def _remove(self) -> dict:
        try:
            return CouchDB.deleteDocument(database=self._database, document=self._key)
        except Exception as e:
            self._logger.error(e)
            return {}

    def _getAll(self) -> list[dict]:
        try:
            return CouchDB.getAllDocuments(database=self._database)
        except Exception as e:
            self._logger.error(e)
            return []