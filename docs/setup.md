# CollabAI — Local setup

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL
- Redis Stack (cache, Celery broker, optional vector search for RAG)

## Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

The backend uses PostgreSQL for local development and tests. Do not use SQLite
database files. After pulling changes, each developer should install
requirements and run migrations against PostgreSQL:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Edit `backend/.env`:

| Variable | Purpose |
|----------|---------|
| `GROQ_MODEL` | Default model (e.g. `llama-3.1-8b-instant`) |
| `DB_HOST` | PostgreSQL host (default `localhost`) |
| `DB_PORT` | PostgreSQL port (default `5432`) |
| `DB_NAME` | PostgreSQL database name (default `collabai_db`) |
| `DB_USER` | PostgreSQL user (default `postgres`) |
| `DB_PASSWORD` | PostgreSQL password (default `12345678` in local `DEBUG=True`) |
| `SECRET_KEY` | Required for every backend start, including local development. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `REDIS_URL` | **Required for production caching** — list/dashboard cache + vector store |
| `CACHE_DEFAULT_TIMEOUT` | List/dashboard TTL in seconds (default `300`) |

Verify Groq connectivity:

```bash
python manage.py check_groq
```

Verify Redis (required for caching demo / requirement #17):

```bash
python manage.py check_redis
```

Start Redis Stack locally, then set `REDIS_URL=redis://127.0.0.1:6379/0` in `backend/.env`.

**Windows (slow login / `check_redis` fails):** Hyper-V may reserve port **6379**, so Docker cannot publish it and Django waits ~10–15s per request on cache/throttle timeouts. Either:

- Comment out `REDIS_URL` in `backend/.env` (uses fast in-memory cache for local dev), or
- Use a free host port, e.g. in project root `.env`: `REDIS_PUBLISH_PORT=16379`, then in `backend/.env`: `REDIS_URL=redis://127.0.0.1:16379/0`, and run `docker compose up redis -d --force-recreate`.

Run migrations and server:

```bash
python manage.py migrate
python manage.py runserver
```

Swagger: `http://127.0.0.1:8000/api/docs/`

## Frontend

```bash
cd frontend
npm install
cp .env.example .env
```

Set `REACT_APP_API_URL=http://127.0.0.1:8000/api/v1` in `frontend/.env`, then:

```bash
npm start
```

## Optional: Celery worker

```bash
cd backend
celery -A config worker -l info
celery -A config beat -l info
```

Set `CELERY_TASK_ALWAYS_EAGER=false` in `.env` when running workers for real async behavior.
