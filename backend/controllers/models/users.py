from urllib import response
from controllers.helpers.login_helpers import login_required, maintainer_required
from models.user import User, Role
from models.image import Image
from models.experiment import Experiment
from models.report import Report
from models.report_data import ReportData
from utilities.security import Password

from flask import Response, Blueprint, request, jsonify, session

users_api = Blueprint("models-users", __name__, url_prefix="/info/users")


@users_api.route("/", methods=("GET", ))
@maintainer_required
def users():
    return jsonify([user.toDict() for user in User.getAll()])


@users_api.route("/<username>", methods=("GET",))
@login_required
def user(username: str):
    """
    Get or update a user's info
    """
    user: User = User.get(username)
    
    if username != session["username"]:
        return Response("You don't have the permission to request this user's info", status=401)
    elif user is None:
        return Response("Couldn't find user", status=404)

    user.password = None
    return jsonify(user.toDict())


@users_api.route("/<username>", methods=("POST",))
@login_required
def update_user(username: str):
    """
    Update a user's info
    """
    loggedInUser: User = User.get(session["username"])
    if not loggedInUser.isMaintainer() and loggedInUser.username != username:
        return Response("Unauthorized access to user info", 403)

    user: User = User.get(username)
    
    if user is None:
        return Response("Couldn't find user", status=404)

    data: dict = request.get_json()
    if data.get("first_name") is None or type(data.get("first_name")) is not str:
        return Response("No first name has been provided.", status=400)
    elif data.get("last_name") is None or type(data.get("last_name")) is not str:
        return Response("No last name has been provided.", status=400)
    elif data.get("role") is None or type(data.get("role")) is not int:
        return Response("No role has been provided.", status=400)

    try:
        user.role = Role(data.get("role"))
    except Exception as e:
        return Response(f"Invalid role was provided: {e}")

    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")

    if not user.update():
        return Response("Couldn't update user info.", status=500)

    return Response(status=200)


@users_api.route("/", methods=("PUT",))
@maintainer_required
def create_user():
    data: dict = request.get_json()

    user: User = User.fromDict({
        "username": data.get("username"),
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "password": data.get("password"),
        "role": data.get("role")
    })

    if user is None:
        return Response("Information is missing or incorrect.", status=400)
    elif user.exists():
        return Response("User already exists", status=409)

    user.password = Password.hashPassword(user.password)
    if not user.create():
        return Response("Could not create user.", status=500)

    return Response(status=200)


@users_api.route("/<username>", methods=("DELETE",))
@maintainer_required
def delete_user(username: str):
    """
    Delete a user's info
    """
    user: User = User.get(username)
    if user is None:
        return Response("User doesn't exists", status=400)
    elif not user.remove():
        return Response("Could not remove user.", status=500)

    experiments: list[Experiment] = Experiment.getAll()
    reports: list[Report] = Report.getAll()
    reports_data: list[ReportData] = ReportData.getAll()

    for experiment in experiments:
        if experiment.user == user.username:
            experiment.remove()

    for report in reports:
        if report.user == user.username:
            report.remove()

    for report_data in reports_data:
        if report_data.user == user.username:
            report_data.remove()

    return Response(status=200)


@users_api.route("/<username>/password", methods=("POST",))
@login_required
def change_password(username: str):
    """
    Changes a user's password
    """
    user: User = User.get(username)
    asker: User = User.get(session["username"])

    if (username != session["username"]) and (not asker.isMaintainer()):
        return Response("You don't have the permission to request this user's info", status=401)
    elif user is None:
        return Response("Couldn't find user", status=404)

    data: dict = request.get_json()

    if type(data.get("password")) is not str:
        return Response("Bad information has been provided.", status=400)

    user.password = Password.hashPassword(data.get("password"))
    if not user.update():
        return Response("Couldn't update user info.", status=500)

    return Response(status=200)


# TODO: Optimize using CouchDB filtering
@users_api.route("/images", methods=("GET", ))
@maintainer_required
def users_image():
    users: list[User] = User.getAll()
    images: list[dict] = []

    for user in users:
        image: Image = Image(user.username).get()
        if image is None:
            continue

        images.append(image.toDict())

    return jsonify(images)


@users_api.route("/<username>/image", methods=("GET", "PUT"))
@login_required
def user_image(username: str):
    user: User = User.get(username)
    if username != session["username"]:
        return Response("You don't have permission to request/change this user image", status=401)
    elif user is None:
        return Response("Couldn't find user", status=404)

    if request.method == "GET":
        image: Image = Image.get(username)
        if image is None:
            return Response("Couldn't find image", status=404)

        return jsonify(image.toDict())
    elif request.method == "PUT":
        data: dict = request.get_json()
        if data.get("image") is None:
            return Response("No image has been provided", status=400)

        image: Image = Image.fromDict({
            "name": username,
            "image": data.get("image")
        })
        if not image.update():
            return Response("Couldn't update image", status=500)

        return Response(status=200)

    return Response("Unknown method", status=400)