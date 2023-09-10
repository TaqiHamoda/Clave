from datetime import datetime
from controllers.helpers.login_helpers import login_required, getLoggedInUser

from models.module import Module
from models.configuration import Configuration
from models.user import User
from models.experiment import Experiment

from engines.module.module_handler import ModuleHandler
from engines.module.module_info import ModuleInfo
from engines.module.module_messages import Commands, ModuleRequest

from utilities.environment import ENV

from flask import Response, Blueprint, request, jsonify

devices_api = Blueprint("devices", __name__, url_prefix="/devices")

@devices_api.route("/<module_name>/<command_id>", methods=("POST",))
@login_required
def devices_command(module_name: str, command_id: str):
    # TODO: Use Configuration engine to verify params match device config
    module: Module = Module.get(module_name)
    configuration: Configuration = Configuration.get(module_name)

    if (module is None) or (configuration is None):
        return Response("Device not found.", status=404)
    elif not ModuleInfo.exists(module.name):
        return Response("Can't find ModuleInfo for device.", status=500)

    user: User = getLoggedInUser()
    module_info: ModuleInfo = ModuleInfo.load(module.name)

    if user == None:
        return Response("User is not logged in.", status=400)
    
    try:
        command: Commands = Commands(command_id)
        data: dict = request.get_json()
        
        parameters: tuple = ()
        experiment_name: str = ''

        if command == Commands.run:
            if data == None:
                return Response("No data provided", 401)

            experiment_name = data.get("name", None)
            exp_parameters: dict = data.get("parameters", None)

            if experiment_name is None:
                return Response("Experiment Name hasn't been provided.", status=401)
            elif exp_parameters is None:
                return Response("Experiment Parameters hasn't been provided.", status=401)
            elif Experiment.get(f"{user.username}-{experiment_name}") is None:
                experiment: Experiment = Experiment.fromDict({
                    "name": experiment_name,
                    "user": user.username,
                    "module": module.name,
                    "timestamp": datetime.now().isoformat(),
                    "parameters": exp_parameters,
                })
                parameters = (experiment.parameters, )

                if not experiment.create():
                    return Response("Couldn't create the experiment.", 500)
            else:
                return Response(f"Experiment {experiment_name} already exists.", status=401)
        elif command == Commands.execute:
            if data == None:
                return Response("No data provided", 401)

            exec_command: str = data.get("command", None)
            exec_parameters: dict = data.get("parameters", None)

            parameters = (exec_command, exec_parameters)

            if exec_command == None:
                return Response("Execute Command hasn't been provided.", status=401)
            elif exec_parameters == None:
                return Response("Execute Parameters hasn't been provided.", status=401)


        elif command == Commands.changeSettings:
            if data == None:
                return Response("No data provided", 401)

            new_settings: dict = data.get("settings", None)

            parameters = (new_settings, )

            if new_settings == None:
                return Response("New Settings hasn't been provided.", status=401)

        module_request = ModuleRequest.fromDict({
            "username": user.username,
            "report": experiment_name,
            "module": module.name,
            "command": command.value,
            "parameters": parameters
        })

        return jsonify(ModuleHandler.execute(module_request, module_info).toDict())
    except Exception as e:
        return Response(f"Server error: {e}", status=500)
