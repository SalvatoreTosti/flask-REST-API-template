from flask import make_response, jsonify

api_base_url = "/api/v1.0"


def not_found(message="Not found"):
    return make_response(jsonify({"error": message}), 404)


def bad_request(message="Bad request"):
    return make_response(jsonify({"error": message}), 400)


def unauthorized(message="Unauthorized"):
    return make_response(jsonify({"error": message}), 401)


def conflict(message="Conflict"):
    return make_response(jsonify({"error": message}), 409)


def method_not_allowed(message="Method not allowed"):
    return make_response(jsonify({"error": message}), 405)


def json_argument_check_str(keys, request):
    for key in keys:
        if not request.json.get(key):
            continue
        if key in request.json and type(request.json[key]) is not str:
            return False
    return True


def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    return True


def json_argument_check_integer(keys, request):
    for key in keys:
        if key in request.json and not is_int(request.json[key]):
            return False
    return True


def json_argument_check_date(keys, request):
    for key in keys:
        if key in request.json and not is_date(request.json[key]):
            return False
    return True
