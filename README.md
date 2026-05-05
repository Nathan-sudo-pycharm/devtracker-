# DevTracker API

A production-quality REST API built with **FastAPI**, **PostgreSQL**, **Docker**, and **GitHub Actions CI/CD**.

Users can register, log in with JWT authentication, and manage tasks via protected endpoints.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (Python) |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Containerization | Docker + docker-compose |
| Testing | pytest + httpx |
| CI/CD | GitHub Actions |

---

## Project Structure

```
devtracker/
├── app/
│   ├── main.py          # App entry point, router registration
│   ├── database.py      # DB connection, session, Base
│   ├── models.py        # SQLAlchemy models (User, Task)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # JWT + password hashing logic
│   └── routers/
│       ├── auth.py      # POST /auth/register, /auth/login
│       └── tasks.py     # Full CRUD for /tasks (protected)
├── tests/
│   ├── conftest.py      # pytest setup, TestClient fixture
│   ├── test_auth.py     # Auth endpoint tests
│   └── test_tasks.py    # Task endpoint tests
├── alembic/             # Database migration files
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI pipeline
├── Dockerfile           # App container definition
├── docker-compose.yml   # App + DB orchestration
├── requirements.txt
├── pytest.ini
└── .env                 # Environment variables (not committed)
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/` | No | Health check |
| GET | `/status` | No | App name and version |
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Login, returns JWT token |
| GET | `/tasks/` | Yes | Get all tasks |
| POST | `/tasks/` | Yes | Create a task |
| GET | `/tasks/{id}` | Yes | Get a specific task |
| PUT | `/tasks/{id}` | Yes | Update a task |
| DELETE | `/tasks/{id}` | Yes | Delete a task |

---

## Getting Started

### Prerequisites
- Docker Desktop installed and running

### Run with Docker

```bash
# Clone the repo
git clone https://github.com/Nathan-sudo-pycharm/devtracker-.git
cd devtracker-

# Create .env file
echo "DATABASE_URL=postgresql://nathan:secret@db:5432/devtracker" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env

# Start app + database
docker-compose up --build
```

App runs at: `http://localhost:8080`  
Swagger docs at: `http://localhost:8080/docs`

### Run Migrations

```bash
alembic upgrade head
```

### Run Tests

```bash
pytest tests/ -v
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret key for signing JWT tokens |

---

## CI/CD

GitHub Actions runs automatically on every push to `main`:
1. Spins up PostgreSQL service container
2. Installs dependencies
3. Runs Alembic migrations
4. Executes all pytest tests

---

## Author

**Nathan Ivor Sequeira**  
[GitHub](https://github.com/Nathan-sudo-pycharm) | [Portfolio](https://nathansequeirafinal.vercel.app/) | nathansequeirade@gmail.com
