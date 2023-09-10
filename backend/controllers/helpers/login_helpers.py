from models.user import User

from functools import wraps
from flask import session, Response

def getLoggedInUser() -> User | None:
    username: str = session.get("username")

    if username is None:
        return None

    user: User = User.get(username)
    if user is not None:  # Renew the session if user is logged in
        session.modified = True

    return user

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if getLoggedInUser() is None:
            return Response("Login required", status=403)
        return f(*args, **kwargs)
    return wrapper


def maintainer_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user: User = getLoggedInUser()
        if user is None:
            return Response("Login required", status=403)
        elif not user.isMaintainer():
            return Response("Must be a maintainer", status=403)

        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user: User = getLoggedInUser()
        if user is None:
            return Response("Login required", status=403)
        elif not user.isAdmin():
            return Response("Must be an admin", status=403)
        return f(*args, **kwargs)
    return wrapper


