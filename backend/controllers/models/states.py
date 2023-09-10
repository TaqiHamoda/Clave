from controllers.helpers.login_helpers import login_required
from models.state import State

from flask import Response, Blueprint, jsonify

states_api = Blueprint("models-states", __name__, url_prefix="/info/states")

@states_api.route("/", methods=("GET",))
@login_required
def states():
    """
    Gets all states
    """
    return jsonify([state.toDict() for state in State.getAll()])

@states_api.route("/<module_id>", methods=("GET",))
@login_required
def state(module_id: str):
    """
    Gets a specific state
    """
    state: State = State.get(module_id)

    if state is None:
        return Response("State not found.", status=404)

    return jsonify(state.toDict())