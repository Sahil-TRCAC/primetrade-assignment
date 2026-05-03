# 🚀 TaskManager API — Production-Ready Backend System

A production-ready **Task Management REST API** built with Flask, designed with secure authentication, scalable architecture, and real-world deployment practices.

This project demonstrates backend engineering fundamentals including **JWT authentication, role-based access control, database integration, and deployment on cloud infrastructure (Render).**

---

## 🌐 Live API

https://primetrade-assignment-kcx0.onrender.com

### Health Check
GET /api/v1/health

---

## ⚙️ Tech Stack

**Backend**
- Flask (Python)
- REST API Architecture
- Flask-JWT-Extended (Authentication)
- Flask-SQLAlchemy (ORM)
- Flask-Bcrypt (Password Security)

**Database**
- PostgreSQL (Production)
- SQLite (Local Development)

**Infrastructure & Tools**
- Gunicorn (WSGI Server)
- Render (Cloud Deployment)
- Postman (API Testing)
- Git & GitHub (Version Control)

---

## 🔐 Core Features

### 🔑 Authentication & Security
- JWT-based authentication (stateless)
- Secure password hashing using bcrypt
- Token-protected routes
- Token expiration handling

---

### 👥 Role-Based Access Control
- User and Admin roles
- Admin-level access to system-wide data
- User-specific task isolation

---

### 📋 Task Management (Full CRUD)
- Create, read, update, and delete tasks
- Persistent storage using PostgreSQL
- User-linked task ownership

---

### 🧱 Backend Architecture
- Modular Flask application structure
- API versioning (/api/v1)
- Clean separation of concerns (routes, models, utils)
- Centralized error handling

---

### ☁️ Production Deployment
- Deployed on Render with Gunicorn
- Environment-based configuration (.env)
- PostgreSQL integration in production
- Debugged real-world deployment issues:
  - Missing dependencies
  - Database initialization
  - Token validation errors
  - Port binding issues

---

## 📡 API Endpoints

### 🔐 Authentication

POST   /api/v1/auth/register  
POST   /api/v1/auth/login  
GET    /api/v1/auth/me  

---

### 📋 Tasks

GET    /api/v1/tasks  
POST   /api/v1/tasks  
PUT    /api/v1/tasks/{id}  
DELETE /api/v1/tasks/{id}  

---

## 🧪 Example Workflow

1. Register → Create user  
2. Login → Receive JWT token  
3. Use token → Access protected routes  
4. Perform CRUD operations on tasks  

---

## 📁 Project Structure
