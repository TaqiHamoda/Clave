from controllers.helpers.login_helpers import login_required, getLoggedInUser
from models.experiment import Experiment
from models.user import User

from flask import Response, Blueprint, jsonify, session

experiments_api = Blueprint("models-experiments", __name__, url_prefix="/info/experiments")

@experiments_api.route("/", methods=("GET",))
@login_required
def experiments():
    """
    Gets all experiments
    """
    experiments: list[dict] = []

    for experiment in Experiment.getAll():
        if experiment.user == session["username"]:
            experiments.append(experiment.toDict())

    return jsonify(experiments)

@experiments_api.route("/<experiment_id>", methods=("GET",))
@login_required
def experiment(experiment_id: str):
    """
    Gets a specific experiment
    """
    user: User = getLoggedInUser()

    if user == None:
        return Response("Unauthorized", 403)

    experiment: Experiment = Experiment.get(f"{user.username}-{experiment_id}")
        
    if experiment is None:
        return Response("Experiment not found.", status=404)

    return jsonify(experiment.toDict())

    