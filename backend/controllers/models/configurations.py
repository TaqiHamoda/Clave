from controllers.helpers.login_helpers import login_required
from models.module import Module
from models.configuration import Configuration

from flask import Response, Blueprint, jsonify

configurations_api = Blueprint("models-configurations", __name__, url_prefix="/info/configurations")

@configurations_api.route("/", methods=("GET",))
@login_required
def configurations():
    """
    Gets all configurations
    """
    return jsonify([config.toDict() for config in Configuration.getAll()])

@configurations_api.route("/<module_id>", methods=("GET",))
@login_required
def configuration(module_id: str):
    """
    Gets a specific configuration
    """
    configuration: Configuration = Configuration.get(module_id)

    if configuration is None:
        return Response("Configuration not found.", status=404)

    return jsonify(configuration.toDict())