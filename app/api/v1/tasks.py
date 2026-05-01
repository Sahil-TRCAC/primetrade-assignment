import logging
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Task, User
from app.utils import success_response, error_response, admin_required

logger = logging.getLogger(__name__)
tasks_bp = Blueprint("tasks", __name__)

VALID_STATUSES = {"pending", "in_progress", "done"}


def validate_task_input(data, partial=False):
    errors = {}
    if not partial or "title" in data:
        title = data.get("title", "")
        if not title or len(title.strip()) < 2:
            errors["title"] = "Title must be at least 2 characters"
    if "status" in data and data["status"] not in VALID_STATUSES:
        errors["status"] = f"Status must be one of: {', '.join(VALID_STATUSES)}"
    return errors


@tasks_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())   # ✅ FIX
    user = User.query.get(user_id)

    if user.role == "admin":
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()

    return success_response([t.to_dict() for t in tasks])


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())   # ✅ FIX
    user = User.query.get(user_id)
    task = Task.query.get(task_id)

    if not task:
        return error_response("Task not found", 404)
    if user.role != "admin" and task.user_id != user_id:
        return error_response("Access denied", 403)

    return success_response(task.to_dict())


@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())   # ✅ FIX
    data = request.get_json()

    if not data:
        return error_response("Request body must be JSON", 400)

    errors = validate_task_input(data)
    if errors:
        return error_response("Validation failed", 422, errors)

    task = Task(
        title=data["title"].strip(),
        description=data.get("description", "").strip(),
        status=data.get("status", "pending"),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    logger.info(f"Task created by user {user_id}: {task.title}")
    return success_response(task.to_dict(), "Task created", 201)


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())   # ✅ FIX
    user = User.query.get(user_id)
    task = Task.query.get(task_id)

    if not task:
        return error_response("Task not found", 404)
    if user.role != "admin" and task.user_id != user_id:
        return error_response("Access denied", 403)

    data = request.get_json()
    if not data:
        return error_response("Request body must be JSON", 400)

    errors = validate_task_input(data, partial=True)
    if errors:
        return error_response("Validation failed", 422, errors)

    if "title" in data:
        task.title = data["title"].strip()
    if "description" in data:
        task.description = data["description"].strip()
    if "status" in data:
        task.status = data["status"]

    db.session.commit()
    logger.info(f"Task {task_id} updated by user {user_id}")
    return success_response(task.to_dict(), "Task updated")


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())   # ✅ FIX
    user = User.query.get(user_id)
    task = Task.query.get(task_id)

    if not task:
        return error_response("Task not found", 404)
    if user.role != "admin" and task.user_id != user_id:
        return error_response("Access denied", 403)

    db.session.delete(task)
    db.session.commit()

    logger.info(f"Task {task_id} deleted by user {user_id}")
    return success_response(message="Task deleted")


# Admin-only: view all users
@tasks_bp.route("/admin/users", methods=["GET"])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    return success_response([u.to_dict() for u in users])