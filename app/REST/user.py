from flask import jsonify, request, url_for, g
from app import app
from app.models.user import User
from app.REST.RESTAuthenticationInterface import auth
from app.REST.utils import api_base_url, not_found, bad_request, unauthorized

base_url = api_base_url + "/users"


@app.route(base_url, methods=["GET"])
@app.route(base_url + "/", methods=["GET"])
def _get_users():
    return get_users()


def get_users():
    return jsonify({"users": [user.to_json() for user in User.query.all()]})


@app.route(base_url + "/<int:user_id>", methods=["GET"])
@auth.login_required
def _get_user(user_id):
    return get_user(user_id)


def get_user(user_id):
    users = [user.to_json() for user in User.query.all() if user.id == user_id]
    if len(users) == 0:
        return not_found()
    if g.user.id != user_id:
        return unauthorized()
    return jsonify({"user": g.user.to_json()})


@app.route(base_url, methods=["POST"])
def _create_user():
    return create_user()


def create_user():
    if (
        not request.json
        or not "username" in request.json
        or not "password" in request.json
    ):
        return bad_request()
    json = request.json
    return (
        jsonify(
            User.make_user(
                username=json["username"], password=json["password"]
            ).to_json()
        ),
        201,
    )


@app.route(base_url + "/<int:user_id>", methods=["PUT"])
@auth.login_required
def _update_user(user_id):
    return update_user(user_id)


def update_user(user_id):
    users = [user for user in User.query.all() if user.id == user_id]
    if len(users) == 0:
        return not_found()
    if not request.json:
        return bad_request()
    if "username" in request.json and type(request.json["username"]) is not str:
        return bad_request()
    if "password" in request.json and type(request.json["password"]) is not str:
        return bad_request()
    if g.user.id != user_id:
        return unauthorized()
    user = g.user

    username = request.json.get("username")
    if username != "":
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            bad_request("Username already in use.")
        else:
            user.set_username(username)

    if request.json.get("password"):
        user.set_password(request.json.get("password"))

    return jsonify({"user": user.to_json()})


@app.route(base_url + "/<int:user_id>", methods=["DELETE"])
@auth.login_required
def _delete_user(user_id):
    return delete_user(user_id)


def delete_user(user_id):
    users = [user for user in User.query.all() if user.id == user_id]
    if len(users) == 0:
        return not_found()
    if g.user.id != user_id:
        return unauthorized()
    user = g.user
    user.delete()
    return jsonify({"result": True})
