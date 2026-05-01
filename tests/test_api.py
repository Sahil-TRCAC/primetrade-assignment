import pytest
import json
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register_user(client, username="testuser", email="test@test.com", password="password123"):
    return client.post("/api/v1/auth/register", json={
        "username": username, "email": email, "password": password
    })


def login_user(client, email="test@test.com", password="password123"):
    return client.post("/api/v1/auth/login", json={
        "email": email, "password": password
    })


# ---- Auth Tests ----

def test_register_success(client):
    res = register_user(client)
    assert res.status_code == 201
    data = res.get_json()
    assert data["status"] == "success"
    assert data["data"]["username"] == "testuser"
    assert data["data"]["role"] == "user"


def test_register_duplicate_email(client):
    register_user(client)
    res = register_user(client)
    assert res.status_code == 409


def test_register_invalid_data(client):
    res = client.post("/api/v1/auth/register", json={"username": "x", "email": "bad", "password": "12"})
    assert res.status_code == 422
    data = res.get_json()
    assert "errors" in data


def test_login_success(client):
    register_user(client)
    res = login_user(client)
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data["data"]


def test_login_wrong_password(client):
    register_user(client)
    res = login_user(client, password="wrongpassword")
    assert res.status_code == 401


def test_me_endpoint(client):
    register_user(client)
    login_res = login_user(client)
    token = login_res.get_json()["data"]["access_token"]
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.get_json()["data"]["email"] == "test@test.com"


def test_me_no_token(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401


# ---- Task Tests ----

def get_token(client):
    register_user(client)
    res = login_user(client)
    return res.get_json()["data"]["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_task(client):
    token = get_token(client)
    res = client.post("/api/v1/tasks", json={"title": "Test Task", "description": "Do this"}, headers=auth_headers(token))
    assert res.status_code == 201
    assert res.get_json()["data"]["title"] == "Test Task"


def test_create_task_invalid(client):
    token = get_token(client)
    res = client.post("/api/v1/tasks", json={"title": "x"}, headers=auth_headers(token))
    assert res.status_code == 422


def test_get_tasks(client):
    token = get_token(client)
    client.post("/api/v1/tasks", json={"title": "Task One"}, headers=auth_headers(token))
    res = client.get("/api/v1/tasks", headers=auth_headers(token))
    assert res.status_code == 200
    assert len(res.get_json()["data"]) == 1


def test_update_task(client):
    token = get_token(client)
    create = client.post("/api/v1/tasks", json={"title": "Old Title"}, headers=auth_headers(token))
    task_id = create.get_json()["data"]["id"]
    res = client.put(f"/api/v1/tasks/{task_id}", json={"title": "New Title", "status": "done"}, headers=auth_headers(token))
    assert res.status_code == 200
    assert res.get_json()["data"]["title"] == "New Title"
    assert res.get_json()["data"]["status"] == "done"


def test_delete_task(client):
    token = get_token(client)
    create = client.post("/api/v1/tasks", json={"title": "To Delete"}, headers=auth_headers(token))
    task_id = create.get_json()["data"]["id"]
    res = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers(token))
    assert res.status_code == 200
    get_res = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers(token))
    assert get_res.status_code == 404


def test_task_not_found(client):
    token = get_token(client)
    res = client.get("/api/v1/tasks/999", headers=auth_headers(token))
    assert res.status_code == 404


def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
