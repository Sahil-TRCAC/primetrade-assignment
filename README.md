# TaskManager — Primetrade.ai Backend Intern Assignment

This project is a full-stack task management application built as part of the Primetrade.ai Backend Intern assignment.

It focuses on building a clean, secure REST API with proper authentication, along with a simple but functional frontend to interact with it.

---

## 🚀 Tech Stack

* **Backend:** Flask (Python)
* **Authentication:** JWT (Flask-JWT-Extended)
* **Database:** SQLite (can be upgraded to PostgreSQL)
* **ORM:** Flask-SQLAlchemy
* **Password Security:** Flask-Bcrypt
* **Frontend:** Vanilla JavaScript, HTML, CSS
* **Testing:** Pytest

---

## ✨ Features

* User registration and login with JWT authentication
* Role-based access control (user vs admin)
* Full CRUD operations for tasks
* Admin can view all users and tasks
* Secure password hashing (bcrypt)
* Structured API responses
* Simple responsive frontend

---

## 📁 Project Structure

```
primetrade_assignment/
├── app/
│   ├── api/v1/         # Routes (auth + tasks)
│   ├── models/         # Database models
│   ├── utils/          # Helpers & decorators
│   ├── config.py       # Configuration
│   └── __init__.py     # App factory
├── frontend/           # UI (index.html)
├── tests/              # Pytest test cases
├── run.py              # Entry point
├── requirements.txt
├── .env.example
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/task-manager.git
cd task-manager
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate (Mac/Linux)
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment

```bash
cp .env.example .env
```

---

### 5. Run backend

```bash
python run.py
```

Backend runs on:

```
http://localhost:5000
```

---

### 6. Run frontend

```bash
cd frontend
python -m http.server 5500
```

Open:

```
http://localhost:5500
```

---

## 🧪 How to Use

1. Register a new account
2. Login using credentials
3. Create tasks from dashboard
4. Edit or delete tasks
5. Admin can view all users

---

## 📡 API Overview

Base URL:

```
http://localhost:5000/api/v1
```

### Auth

* `POST /auth/register`
* `POST /auth/login`
* `GET /auth/me`

### Tasks

* `GET /tasks`
* `POST /tasks`
* `PUT /tasks/:id`
* `DELETE /tasks/:id`

---

## 🔐 Security Notes

* Passwords are hashed using bcrypt
* JWT tokens expire after a set time
* Role-based access control enforced
* No secrets are hardcoded

---

## 🧠 Notes

This project was built with simplicity and clarity in mind.
The goal was not just to make it work, but to keep the structure clean and easy to understand.

---

## 📸 Screenshots  
<img width="1874" height="976" alt="image" src="https://github.com/user-attachments/assets/7609df84-5d88-4b53-879f-0e411b61b638" />
<img width="1556" height="997" alt="image" src="https://github.com/user-attachments/assets/052af453-aeb7-4f7d-9793-d3a211f49f68" />
<img width="1918" height="1026" alt="image" src="https://github.com/user-attachments/assets/eb73b18c-be8b-4456-af09-65a577e9b600" />
<img width="1911" height="980" alt="image" src="https://github.com/user-attachments/assets/42cc78da-0ec0-4f3c-ba3f-0798b0c7c295" />

  








+
