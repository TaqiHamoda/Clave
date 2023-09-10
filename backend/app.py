from utilities.security import Password
from utilities.environment import ENV

from models.image import Image
from models.module import Module
from models.user import User, Role
from models.configuration import Configuration
from models.device import Device

from utilities.couchdb import CouchDB
from engines.module.module_handler import ModuleHandler
from engines.module.module_info import ModuleInfo
from engines.module.module_messages import ModuleRequest, ModuleResponse, Commands

from controllers.blueprints import MODELS_BLUEPRINTS, SERVICES_BLUEPRINTS

import os, logging,  datetime,  atexit
from flask import Flask
from flask_session import Session
from flask_cors import CORS

logger: logging.Logger = logging.getLogger()


def initializeDB() -> None:
    CouchDB.changeSettings(
        user=ENV.db_user,
        password=ENV.db_password,
        port=ENV.db_port,
        url=ENV.db_address,
        timeout=ENV.db_timeout,
        https=ENV.db_https_enabled
    )

    try:
        CouchDB.getInfo()
    except Exception as e:
        logger.error(e)


def loadAndRunModules() -> None:
    for dir_name in os.listdir(ENV.module_path):
        Module.loadFromDir(dir_name)

    ModuleInfo.initialize()

    for module in Module.getAll():
        if ModuleInfo.exists(module.name):
            continue

        module_info: ModuleInfo = ModuleInfo(module.name)
        module_handler: ModuleHandler = ModuleHandler(module_info)

        module_handler.run(module.dir_name)
        
        logger.info(f"ModuleHandler {module.name} is initialized")
        


def updateModulesDB() -> None:
    for module in Module.getAll():
        module_info: ModuleInfo = ModuleInfo.load(module.name)
        module_handler: ModuleHandler = ModuleHandler(module_info)

        request: ModuleRequest = ModuleRequest.fromDict({
            "username": ENV.admin_username,
            "report": "",
            "module": module.name,
            "command": Commands.getStatus,
            "parameters": ()
        })

        response: ModuleResponse = module_handler.execute(request, module_info)
        if not response.success:
            logger.error(f"Could not get Status of module {module.name}.")
            continue
        
        request.command = Commands.getSettings
        response: ModuleResponse = module_handler.execute(request, module_info)
        if not response.success:
            logger.error(f"Could not get Settings of module {module.name}.")
            continue

        request.command = Commands.getState
        response: ModuleResponse = module_handler.execute(request, module_info)
        if not response.success:
            logger.error(f"Could not get State of module {module.name}.")
            continue

        logger.info(f"{module.name} module has been updated")


def initializeAdminUser() -> None:
    if len(User.getAll()) > 0:
        return None

    admin: User = User.fromDict({
        "username": ENV.admin_username,
        "first_name": "",
        "last_name": "",
        "password": Password.hashPassword(ENV.admin_username),
        "role": Role.admin
    })

    if (admin is None) or (not admin.create()):
        raise Exception("Couldn't create the admin user.")


def cleanup() -> None:
    for module in Module.getAll():
        if not ModuleInfo.exists(module.name):
            continue

        module_info: ModuleInfo = ModuleInfo.load(module.name)
        module_info.dispose()


def initializeServer() -> Flask:
    atexit.register(cleanup)

    # Create log directory if it doesn't exist
    if not os.path.exists(os.path.dirname(ENV.log_file_path)):
        os.mkdir(os.path.dirname(ENV.log_file_path))

    # Setting up Session Settings    
    app: Flask = Flask(__name__)
    
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=ENV.server_inactivity_timeout)
    app.config['SESSION_COOKIE_NAME'] = "session"
    app.config["SECRET_KEY"] = ENV.server_secret
    
    # Initializing the server side session
    app.config.from_object(__name__)
    Session(app).init_app(app)
    CORS(app, supports_credentials=True, origins='*')

    # Registering the model controllers
    for model_blueprint in MODELS_BLUEPRINTS:
        app.register_blueprint(model_blueprint)

    for service_blueprint in SERVICES_BLUEPRINTS:
        app.register_blueprint(service_blueprint)

    # Methods to run before the first request to the server
    app.before_first_request(initializeDB)
    app.before_first_request(initializeAdminUser)
    app.before_first_request(loadAndRunModules)
    app.before_first_request(updateModulesDB)

    return app

app: Flask = initializeServer()

if __name__ == "__main__":
    try:
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S %p",
            level=ENV.server_log_level,
            filename=ENV.log_file_path,
            filemode="a"
        )

        app.run(host=ENV.server_address, port=ENV.server_port, debug=True)
    except Exception as e:
        logger.exception(e)
