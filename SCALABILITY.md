# Scalability & Architecture Notes

## Current Architecture

This project uses a **modular monolith** structure via Flask Blueprints with API versioning (`/api/v1/`). This makes it easy to extract services later.

```
Client → Flask API (v1) → SQLAlchemy ORM → SQLite/PostgreSQL
```

---

## Path to Scale

### 1. Database — SQLite → PostgreSQL
The ORM layer (SQLAlchemy) is database-agnostic. Switching to PostgreSQL requires only a one-line change in `.env`:
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```
No code changes needed.

### 2. Horizontal Scaling — Multiple Instances
Flask is stateless (JWT replaces server-side sessions). This means you can run multiple instances behind a **load balancer** (e.g., Nginx, AWS ALB) with zero shared state issues.

```
            ┌─────────────┐
Clients  →  │ Load Balancer│
            └──────┬──────┘
         ┌─────────┼─────────┐
      Instance1  Instance2  Instance3
         └─────────┼─────────┘
                   │
              PostgreSQL (shared)
```

### 3. Caching — Redis
For high-traffic read endpoints (e.g., `GET /tasks`), add **Redis** caching:
```python
from flask_caching import Cache
cache = Cache(config={"CACHE_TYPE": "redis", "CACHE_REDIS_URL": os.getenv("REDIS_URL")})

@tasks_bp.route("", methods=["GET"])
@cache.cached(timeout=30, key_prefix=lambda: f"tasks_{get_jwt_identity()}")
def get_tasks(): ...
```

### 4. Microservices — Extract by Domain
The Blueprint structure maps cleanly to microservices when needed:

| Blueprint | Future Microservice |
|-----------|---------------------|
| `/api/v1/auth` | Auth Service |
| `/api/v1/tasks` | Task Service |

Each service gets its own database and communicates via REST or a message queue (e.g., RabbitMQ, Kafka).

### 5. Async Task Processing — Celery
For long-running operations (email notifications, report generation):
```python
from celery import Celery
celery = Celery(broker=os.getenv("REDIS_URL"))

@celery.task
def send_task_notification(user_id, task_id): ...
```

### 6. Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
```

Run with:
```bash
docker build -t taskmanager .
docker run -p 5000:5000 --env-file .env taskmanager
```

### 7. New Modules — Adding Features
The project structure is built for extension. Adding a new module (e.g., `projects`) requires:
1. Create `app/api/v1/projects.py` with Blueprint
2. Register in `app/__init__.py` — one line
3. Add model to `app/models/models.py`

No existing code needs to change.

---

## Summary

| Concern | Solution |
|---------|----------|
| Database | PostgreSQL via SQLAlchemy (swap `.env`) |
| Load distribution | Stateless JWT + load balancer |
| Read performance | Redis caching layer |
| Background jobs | Celery + Redis |
| Deployment | Docker + Gunicorn |
| Service growth | Blueprint → Microservice extraction |
