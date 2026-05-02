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
