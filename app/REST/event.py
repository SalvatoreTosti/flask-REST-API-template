import numbers
from flask import jsonify, request, g
from app import app
from app.models.user import User
from app.models.event import Event


from app.REST.RESTAuthenticationInterface import auth
from app.REST.utils import (
    api_base_url,
    json_argument_check_str,
    json_argument_check_integer,
    json_argument_check_date,
    not_found,
    bad_request,
    unauthorized,
)

base_url = api_base_url + "/events"


@app.route(base_url, methods=["GET"])
@app.route(base_url + "/", methods=["GET"])
def _get_events():
    return get_events()


def get_events():
    return jsonify([e.to_json() for e in Event.query.all()])


@app.route(base_url + "/<int:event_id>", methods=["GET"])
@auth.login_required
def _get_event(event_id):
    return get_event(event_id)


def get_event(event_id):
    events = [e for e in Event.query.all() if e.id == event_id]
    if len(events) == 0:
        return not_found()
    event = events[0]
    if g.user.id != event.user_id:
        return unauthorized()
    return jsonify(event.to_json())


@app.route(base_url, methods=["POST"])
@auth.login_required
def _create_event():
    return create_event()


def create_event():
    if (
        not request.json
        or not "user_id" in request.json
        or not isinstance(request.json["user_id"], numbers.Number)
        or not "name" in request.json
        or not "data" in request.json
    ):
        return bad_request()
    json = request.json
    user_id = json["user_id"]
    users = [user.to_json() for user in User.query.all() if user.id == user_id]
    if len(users) == 0:
        return not_found()
    if g.user.id != user_id:
        return unauthorized()
    return (
        jsonify(
            Event.make_event(
                user_id=json["user_id"], name=json["name"], data=json["data"]
            ).to_json()
        ),
        201,
    )


@app.route(base_url + "/<int:event_id>", methods=["PUT"])
@auth.login_required
def _update_event(event_id):
    return update_event(event_id)


def update_event(event_id):
    if not json_argument_check_str(["name"], request):
        return bad_request()

    events = [e for e in Event.query.all() if e.id == event_id]
    if len(events) == 0:
        return not_found()
    event = events[0]

    if g.user.id != event.user_id:
        return unauthorized()

    event.set_fields(request.json)
    return jsonify(event.to_json())


@app.route(base_url + "/<int:event_id>", methods=["DELETE"])
@auth.login_required
def _delete_event(event_id):
    return delete_event(event_id)


def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return not_found()
    if g.user.id != event.user_id:
        return unauthorized()
    event.delete()
    return jsonify({"result": True})
