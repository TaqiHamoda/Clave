from controllers.helpers.login_helpers import maintainer_required, admin_required
from utilities.environment import ENV

from flask import Response, Blueprint, request, jsonify
from datetime import datetime

settings_api = Blueprint("settings", __name__, url_prefix="/settings")


@settings_api.route("/info", methods=("GET", "PUT",))
@maintainer_required
def settings_changeSettings():
    if request.method == "GET":
        return jsonify({
            "max_wait_runtime": ENV.max_wait_runtime,
        })
    elif request.method == "PUT":
        try:
            if request.form["max_wait_runtime"] is not None:
                ENV.max_wait_runtime = float(request.form["max_wait_runtime"])
            
            
            return Response(status=200)
        except Exception as e:
            return Response("Couldn't get set new info. Check that value are correct.", status=500)