from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import User


def success_response(data=None, message="Success", status_code=200):
    response = {"status": "success", "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error_response(message="An error occurred", status_code=400, errors=None):
    response = {"status": "error", "message": message}
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != "admin":
            return error_response("Admin access required", 403)
        return fn(*args, **kwargs)
    return wrapper
