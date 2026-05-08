# API endpoints

**Canonical rule:** all product REST endpoints use prefix **`/api/v1`**. Document tooling lives at **`/api/docs/`** and **`/api/schema/`** (no version segment). GitHub Issues must copy paths from this file to avoid drift.

Base URL (development): `http://127.0.0.1:8000/api/v1`

Swagger UI: `http://127.0.0.1:8000/api/docs/`  
OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Authentication

### Register user

| Item | Value |
|------|--------|
| Story | AUTH-01 |
| Method | `POST` |
| Path | `/auth/register` |
| Full URL | `/api/v1/auth/register` |

**Request body (JSON)**

```json
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

**Success:** `201 Created`

Response body includes `id` and `email`. Password is write-only and never returned.

**Validation errors:** `400 Bad Request`

Typical payload shape:

```json
{
  "email": ["A user with this email already exists."]
}
```

or

```json
{
  "password": ["Password must contain at least one uppercase letter."]
}
```

Password rules combine Django validators plus extra complexity checks (mixed case, digit, special character).

## Projects

| Method | Path | Full URL |
|--------|------|----------|
| `GET` | `/projects/` | `/api/v1/projects/` |
| `POST` | `/projects/` | `/api/v1/projects/` |
| `GET` | `/projects/{id}/` | `/api/v1/projects/{id}/` |
| `PUT` | `/projects/{id}/` | `/api/v1/projects/{id}/` |
| `PATCH` | `/projects/{id}/` | `/api/v1/projects/{id}/` |
| `DELETE` | `/projects/{id}/` | `/api/v1/projects/{id}/` |

List supports pagination, `search`, `ordering`, and filter params: `status`, `created_by`, `start_date`, `due_date`.

## Tasks

| Method | Path | Full URL |
|--------|------|----------|
| `GET` | `/tasks/` | `/api/v1/tasks/` |
| `POST` | `/tasks/` | `/api/v1/tasks/` |
| `GET` | `/tasks/{id}/` | `/api/v1/tasks/{id}/` |
| `PUT` | `/tasks/{id}/` | `/api/v1/tasks/{id}/` |
| `PATCH` | `/tasks/{id}/` | `/api/v1/tasks/{id}/` |
| `DELETE` | `/tasks/{id}/` | `/api/v1/tasks/{id}/` |

List supports pagination, `search`, `ordering`, and filter params: `project`, `status`, `assignee`, `priority`, `due_date`, `completed_at`.

## Comments

| Method | Path | Full URL |
|--------|------|----------|
| `GET` | `/comments/` | `/api/v1/comments/` |
| `POST` | `/comments/` | `/api/v1/comments/` |
| `GET` | `/comments/{id}/` | `/api/v1/comments/{id}/` |
| `PUT` | `/comments/{id}/` | `/api/v1/comments/{id}/` |
| `PATCH` | `/comments/{id}/` | `/api/v1/comments/{id}/` |
| `DELETE` | `/comments/{id}/` | `/api/v1/comments/{id}/` |

List supports pagination, `search`, `ordering`, and filter params: `task`, `author`.

## Activity Logs

| Method | Path | Full URL |
|--------|------|----------|
| `GET` | `/audit/activity/` | `/api/v1/audit/activity/` |
| `GET` | `/audit/activity/{id}/` | `/api/v1/audit/activity/{id}/` |

Activity log endpoint is read-only and supports pagination, `search`, `ordering`, and filter params: `project`, `task`, `comment`, `user`, `action`.
