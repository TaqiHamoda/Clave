from controllers.helpers.login_helpers import maintainer_required
from models.user import Role, User

from flask import Response, Blueprint, request, session

profile_api = Blueprint("profile", __name__, url_prefix="/profile")

@profile_api.route("/<username>/role", methods=("PUT",))
@maintainer_required
def profile_role(username: str):
    user: User = User.get(username)
    asker: User = User.get(session["username"])

    if user is None:
        return Response("Couldn't find user", status=404)

    if type(request.form["role"]) is not str:
        return Response("Bad information has been provided.", status=400)

    try:
        user.role = Role(request.form["role"])
        if user.isAdmin() and not asker.isAdmin():
            return Response("You don't have permission to update this user to admin privileges.", status=401)
        elif not user.update():
            return Response("Couldn't update user info.", status=500)

        return Response(status=200)
    except Exception as e:
        return Response(f"Server error: {e}")