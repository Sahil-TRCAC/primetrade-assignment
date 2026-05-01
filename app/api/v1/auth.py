import logging
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models import User
from app.utils import success_response, error_response

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


def validate_register_input(data):
    errors = {}
    if not data.get("username") or len(data["username"].strip()) < 3:
        errors["username"] = "Username must be at least 3 characters"
    if not data.get("email") or "@" not in data["email"]:
        errors["email"] = "Valid email is required"
    if not data.get("password") or len(data["password"]) < 6:
        errors["password"] = "Password must be at least 6 characters"
    return errors


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return error_response("Request body must be JSON", 400)

    errors = validate_register_input(data)
    if errors:
        return error_response("Validation failed", 422, errors)

    username = data["username"].strip()
    email = data["email"].strip().lower()

    if User.query.filter_by(username=username).first():
        return error_response("Username already taken", 409)
    if User.query.filter_by(email=email).first():
        return error_response("Email already registered", 409)

    role = "admin" if data.get("role") == "admin" and User.query.count() == 0 else "user"
    password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(username=username, email=email, password_hash=password_hash, role=role)
    db.session.add(user)
    db.session.commit()

    logger.info(f"New user registered: {username} ({role})")
    return success_response(user.to_dict(), "User registered successfully", 201)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return error_response("Request body must be JSON", 400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return error_response("Email and password are required", 422)

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return error_response("Invalid email or password", 401)

    access_token = create_access_token(identity=str(user.id))
    logger.info(f"User logged in: {user.username}")
    return success_response({
        "access_token": access_token,
        "user": user.to_dict()
    }, "Login successful")


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)
    return success_response(user.to_dict())
