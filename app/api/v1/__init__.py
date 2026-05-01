from flask import Blueprint
from .auth import auth_bp
from .tasks import tasks_bp

api_v1 = Blueprint("api_v1", __name__)
