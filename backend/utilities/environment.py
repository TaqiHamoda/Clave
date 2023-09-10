from __future__ import annotations

import json
import logging
from pathlib import Path

class Environment:
    _instance: Environment = None

    _PARAMS: dict[str, dict[str, type]] = {
        "server": {
            "address": str,
            "port": int,
            "cert_dir_path": str,
            "log_level": str,
            "secret": str.encode,
            "inactivity_timeout": int,
        },
        "database": {
            "user": str,
            "password": str,
            "port": int,
            "url": str,
            "timeout": float,
            "https_enabled": bool,
        },
        "modules": {
            "user": str,
            "path": str,
            "max_wait_runtime": float,
        },
    }

    # Server Parameters
    server_log_level: logging._Level = None
    server_address: str = None
    server_port: int = None
    server_cert_dir_path: str = None
    server_secret: bytes = None
    server_inactivity_timeout: int = None

    # Database Parameters
    db_user: str = None
    db_password: str = None
    db_port: int = None
    db_url: str = None
    db_timeout: float = None
    db_https_enabled: bool = None

    # Module Engine Parameters
    module_user: str = None
    module_path: str = None
    max_wait_runtime: float = None
    
    # Open-CR Parameters
    open_cr_path: Path = Path(__file__).parent.parent
    max_string_length: int = 256
    module_process_pool_count: int = 4

    # Developer Parameters
    version: str = "0.1-alpha"
    app_name: str = "Open-CR"
    admin_username: str = "admin"

    # Application Parameters
    max_password_len: int = 1024
    downloads_dir_path: str = "../tmp"
    log_file_path: str = f"/var/log/{app_name}/server.log"
    module_handler_pipe_path: str = f"/tmp/{app_name}/"

    def __init__(self) -> None:
        if Environment._instance is not None:
            raise Exception("You can't initialize the Environment. It is a singleton class.")

        with open(f"{self.open_cr_path}/.env.json", 'r') as env_file:
            env_local = json.load(env_file)

            for params in self._PARAMS.keys():
                for param in self._PARAMS[params].keys():
                    if env_local[params][param] is None:
                        raise Exception(f"Parameter {param} is required to be present in the .env.local file")
                
                env_local[params][param] = self._PARAMS[params][param](env_local[params][param])

            self.server_address = env_local["server"]["address"]
            self.server_port = env_local["server"]["port"]
            self.server_cert_dir_path = env_local["server"]["cert_dir_path"]
            self.server_log_level = logging._nameToLevel.get(env_local["server"]["log_level"])
            self.server_secret = str.encode(env_local["server"]["secret"], encoding="utf-8")
            self.server_inactivity_timeout = env_local["server"]["inactivity_timeout"]

            if self.server_log_level is None:
                raise Exception("Incorrect log level has been provided. Please use one of the following: 'CRITICAL', 'FATAL', 'ERROR', 'WARN' or 'WARNING', 'INFO', 'DEBUG'.")

            self.db_user = env_local["database"]["user"]
            self.db_password = env_local["database"]["password"]
            self.db_port = env_local["database"]["port"]
            self.db_url = env_local["database"]["url"]
            self.db_timeout = env_local["database"]["timeout"]
            self.db_https_enabled = env_local["database"]["https_enabled"]

            self.module_user = env_local["modules"]["user"]
            self.module_path = env_local["modules"]["path"]
            self.max_wait_runtime = env_local["modules"]["max_wait_runtime"]
            
        Environment._instance = self

    @staticmethod
    def getInstance():
        if Environment._instance is None:
            Environment()

        return Environment._instance


ENV = Environment.getInstance()

