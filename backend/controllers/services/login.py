from utilities.security import Password
from models.user import User
from controllers.helpers.login_helpers import getLoggedInUser

import json

from flask import request, jsonify, session, Response, Blueprint

login_api = Blueprint("login", __name__, url_prefix="/login")

@login_api.route("/", methods=("GET", "POST", "DELETE"))
def login_login():
    user: User = getLoggedInUser()
    
    if request.method == "POST":
        data = request.get_json()

        if (data.get("username") is None) or (data.get("password") is None):
            return Response("Missing username and password fields", status=400)
        
        user = User.get(data.get("username"))
        if (user is None) or (not Password.isSame(user.password, data.get("password"))):
            return Response("Username or password is incorrect.", status=400)

        session["username"] = user.username
        session.modified = True

        return Response(status=200)
    elif request.method == "GET":
        if user is not None:
            user.password = None
            return jsonify({
                "logged_in": user is not None,
                "user": user.toDict()
            })
        else:
            return jsonify({
                "logged_in": user is not None,
                "user": None
            })
    elif request.method == "DELETE":
        session.pop("username", None)
        return Response(status=200)

    return Response("Method unknown", status=400)
