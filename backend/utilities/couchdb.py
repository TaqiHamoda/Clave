from typing import Callable
import requests, urllib.parse, json, logging

# TODO: Add a getMetadata method that gets the ID and Rev

class CouchDB:  # TODO: Finish the database library
    _timeout: int = None  # Timeout in seconds
    _location: str = None  # Location of the CouchDB server

    _logger: logging.Logger = logging.getLogger()

    @staticmethod
    def changeSettings(password:str, port:str, user:str, url:str, timeout:float=1, https:bool=False) -> None:
        # Encode the username and password so that no issues occur
        user: str = urllib.parse.quote(user, safe="")
        password: str = urllib.parse.quote(password, safe="")

        CouchDB._timeout = timeout

        if https:
            CouchDB._location = "https://"
        else:
            CouchDB._location = "http://"
        
        CouchDB._location += f"{user}:{password}@{url}:{port}/"

    @staticmethod
    def _executeRequest(url_segments:tuple[str], data:dict=None, http_request:str="GET") -> requests.Response:
        if CouchDB._location is None:
            raise Exception("Server location has not been provided. Please change the settings.")
        
        switch: dict[str, Callable] = {
            "DELETE": requests.delete,
            "GET": requests.get,
            "HEAD": requests.head,
            "POST": requests.post,
            "PUT": requests.put,
        }
        
        # Get the appropriate requests method
        req: Callable = switch.get(http_request)
        if req is None:
            raise Exception(f"Invalid HTTP request: {http_request}")

        # Execute request and get response
        url: str = "/".join([urllib.parse.quote(segment, safe="?=") for segment in url_segments])

        if data is not None:
            data = json.dumps(data)

        res: requests.Response = req(CouchDB._location + "/" + url, data=data, timeout=CouchDB._timeout)

        CouchDB._logger.info(f"CouchDB \"[{http_request}] {url}\": {res.status_code}")

        return res

    # CouchDB Methods
    @staticmethod
    def getInfo() -> dict:
        res: requests.Response = CouchDB._executeRequest([], http_request="GET")

        if res.ok:
            return res

        raise Exception(f"Couldn't connect to the database server: {res.reason} {res.text}")

    @staticmethod
    def isDatabase(database:str) -> bool:
        res: requests.Response = CouchDB._executeRequest([database,], http_request="HEAD")
        
        if res.ok:
            return True
        elif res.status_code == 404:
            return False

        raise Exception(f"Couldn't check if database exists: {res.reason} {res.text}")

    @staticmethod
    def getDatabase(database:str) -> dict:
        res: requests.Response = CouchDB._executeRequest((database,), http_request="GET")

        if not res.ok:
            raise Exception(f"Couldn't get database: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def createDatabase(database:str) -> dict:
        res: requests.Response = CouchDB._executeRequest((database,), http_request="PUT")

        if not res.ok:
            raise Exception(f"Couldn't create database: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def deleteDatabase(database:str) -> dict:
        res: requests.Response = CouchDB._executeRequest((database,), http_request="DELETE")

        if not res.ok:
            raise Exception(f"Couldn't delete database: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def getAllDatabases() -> list[str]:
        res: requests.Response = CouchDB._executeRequest(["_all_dbs",], http_request="GET")

        if not res.ok:
            raise Exception(f"Couldn't get all databases: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def isDocument(database:str, document:str) -> bool:
        res: requests.Response = CouchDB._executeRequest((database, document), http_request="HEAD")

        if res.ok:
            return True
        elif res.status_code == 404:
            return False

        raise Exception(f"Couldn't check if document exists: {res.reason} {res.text}")

    @staticmethod
    def getDocument(database:str, document:str) -> dict:
        res: requests.Response = CouchDB._executeRequest((database, document), http_request="GET")

        if not res.ok:
            raise Exception(f"Couldn't get document: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def createDocument(database:str, document:str, data:dict) -> dict:
        res: requests.Response = CouchDB._executeRequest((database, document), http_request="PUT", data=data)

        if not res.ok:
            raise Exception(f"Couldn't create document: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def updateDocument(database:str, document:str, data:dict) -> dict:
        # Need to get the old rev ID
        old_doc = CouchDB.getDocument(database=database, document=document)
        data["_rev"] = old_doc["_rev"]

        res: requests.Response = CouchDB._executeRequest((database, document), http_request="PUT", data=data)

        # If conflict occured, try again.
        if res.status_code == 409:
            return CouchDB.updateDocument(database=database, document=document, data=data)
        elif not res.ok:
            raise Exception(f"Couldn't update document: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def deleteDocument(database:str, document:str) -> dict:
        # Need to get the old rev ID
        old_doc = CouchDB.getDocument(database=database, document=document)
        rev_id = old_doc["_rev"]

        res: requests.Response = CouchDB._executeRequest([database, document + "?rev=" + rev_id], http_request="DELETE")

        if not res.ok:
            raise Exception(f"Couldn't delete document: {res.reason} {res.text}")

        return res.json()

    @staticmethod
    def getAllDocuments(database:str) -> list[str]:
        res: requests.Response = CouchDB._executeRequest([database, "_all_docs?include_docs=true"], http_request="GET")

        if not res.ok:
            raise Exception(f"Couldn't get all documents: {res.reason} {res.text}")

        return res.json()["rows"]

    # Mango Query Methods
    @staticmethod
    def createIndex(database:str, index:dict) -> dict:
        pass

    @staticmethod
    def runQuery(database:str, query:dict) -> dict:
        pass

    # File Attachement Methods
    @staticmethod
    def isFile(database:str, document:str, filename:str) -> dict:
        pass

    @staticmethod
    def getFile(database:str, document:str, filename:str) -> dict:
        pass

    @staticmethod
    def attachFile(database:str, document:str, path:str) -> dict:
        pass

    @staticmethod
    def deleteFile(database:str, document:str, filename:str) -> dict:
        pass