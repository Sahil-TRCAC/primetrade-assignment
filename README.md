# TaskManager API — Primetrade.ai Backend Intern Assignment

A secure, scalable REST API with JWT authentication, role-based access control, and a Vanilla JS frontend.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask 3.0, Python 3.10+ |
| Auth | Flask-JWT-Extended (JWT) |
| ORM | Flask-SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod-ready) |
| Password Hashing | Flask-Bcrypt |
| CORS | Flask-CORS |
| Frontend | Vanilla JS, HTML, CSS |
| Testing | Pytest |

---

## Project Structure

```
primetrade_assignment/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── models/
│   │   └── models.py        # User & Task models
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py      # Register, Login, Me
│   │       └── tasks.py     # CRUD + Admin routes
│   └── utils/
│       └── helpers.py       # Response helpers, role decorator
├── frontend/
│   └── index.html           # Single-page UI
├── tests/
│   └── test_api.py          # 12 pytest test cases
├── run.py                   # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/primetrade-assignment.git
cd primetrade-assignment
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your own secret keys
```

### 5. Run the server
```bash
python run.py
```
API will be available at: `http://localhost:5000`

### 6. Open the frontend
Open `frontend/index.html` in your browser (no server needed).

---

## API Reference (v1)

All endpoints are prefixed with `/api/v1`

### Auth Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Register a new user |
| POST | `/auth/login` | ❌ | Login and get JWT token |
| GET | `/auth/me` | ✅ | Get current user profile |

### Task Endpoints

| Method | Endpoint | Auth | Role | Description |
|--------|----------|------|------|-------------|
| GET | `/tasks` | ✅ | user/admin | Get tasks (admin sees all) |
| GET | `/tasks/:id` | ✅ | user/admin | Get single task |
| POST | `/tasks` | ✅ | user/admin | Create a task |
| PUT | `/tasks/:id` | ✅ | user/admin | Update a task |
| DELETE | `/tasks/:id` | ✅ | user/admin | Delete a task |
| GET | `/tasks/admin/users` | ✅ | admin only | List all users |

### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | API status |

### Response Format
All responses follow a consistent schema:
```json
{
  "status": "success" | "error",
  "message": "Human-readable message",
  "data": { ... }
}
```

---

## Role-Based Access

| Feature | User | Admin |
|---------|------|-------|
| Register / Login | ✅ | ✅ |
| View own tasks | ✅ | ✅ |
| View all tasks | ❌ | ✅ |
| Create task | ✅ | ✅ |
| Edit/Delete own task | ✅ | ✅ |
| Edit/Delete any task | ❌ | ✅ |
| View all users | ❌ | ✅ |

> **Note:** The first user to register with `"role": "admin"` in the request body becomes admin.

---

## Running Tests

```bash
pytest tests/ -v
```

12 test cases covering: registration, login, auth protection, CRUD operations, validation, and error handling.

---

## Security Practices

- Passwords hashed with **bcrypt** (never stored as plain text)
- **JWT tokens** with expiry (1 hour default, configurable)
- All secrets stored in **environment variables** (never hardcoded)
- Input **validation** on all endpoints with structured error messages
- **Role-based access control** enforced via decorator
- **CORS** configured for frontend-backend separation

---

## Scalability Note

See `SCALABILITY.md` for full details on how this project is designed to scale.
