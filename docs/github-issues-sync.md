# GitHub Issues — zero-ambiguity sync (with code)

**Canonical contract:** every HTTP API path in an issue is either (a) **path relative to versioned API** ` /api/v1` **or** (b) explicitly **full path** ` /api/v1/...` . There is **no** bare `/api/...` for product endpoints (only `/api/docs/`, `/api/schema/` for tooling).

**Source of truth in repo:** [api-endpoints.md](./api-endpoints.md) (update it when you add routes).

**Frontend env:** `REACT_APP_API_URL` must be the **base including** `/api/v1` (see `frontend/.env.example`).

---

## One line to add at the top of every API-related issue

```text
API prefix (canonical): https://<host>/api/v1 — paths below are relative unless marked FULL URL.
```

---

## Replace these strings in issue bodies (find → replace)

| Find (ambiguous / wrong for current repo) | Replace with |
|------------------------------------------|--------------|
| `POST /api/auth/register` | `POST /api/v1/auth/register` (FULL: only path under version) |
| `POST /api/auth/login` | `POST /api/v1/auth/login` (planned; not implemented until AUTH-02) |
| `GET /api/projects/` | `GET /api/v1/projects/...` (planned; implement under `apps.projects`) |
| `GET /api/tasks/` | `GET /api/v1/tasks/...` (planned) |
| `GET /api/activity-logs/` | `GET /api/v1/.../activity/` or as designed in API-01 (TBD) |
| `PATCH /api/tasks/{id}/` | `PATCH /api/v1/tasks/<id>/` (planned) |

---

## Per-story edits (paste into GitHub or edit description)

### AUTH-01 — Register API

Add/replace in **Tasks** and **Acceptance**:

```text
Implemented endpoint (canonical):
- POST /api/v1/auth/register  (relative to server root; Axios baseURL must end with /api/v1)

Verification:
- Swagger: /api/docs/ → tag Authentication → POST auth/register
- Tests: cd backend && python manage.py test apps.core

Dependency note: AUTH-02 adds JWT; AUTH-01 remains valid without tokens (201 + user fields).
```

### AUTH-02 — Login + JWT

Add at top:

```text
All auth routes are under /api/v1/auth/...
Planned: POST /api/v1/auth/login, POST /api/v1/auth/refresh, POST /api/v1/auth/logout
(Register remains POST /api/v1/auth/register from AUTH-01.)
```

### MIDDLEWARE-01 — Logging + Auth

Add:

```text
Current repo already has RequestLoggingMiddleware (method, path, status, duration, client IP).
Do not duplicate a second "generic" logger. JWT enforcement should use DRF authentication
classes on views; add request-id / extra fields only if agreed with the team.
```

### FE-01 — React + Context

Add:

```text
API base: REACT_APP_API_URL=http(s)://<host>/api/v1 (copy frontend/.env.example).
AuthContext exposes { user, setUser }; JWT storage is FE-02 scope.
```

### FE-02 — Auth UI

Replace endpoint bullets with:

```text
- POST /api/v1/auth/register (AUTH-01)
- POST /api/v1/auth/login (AUTH-02)
Store tokens only after AUTH-02 lands; extend AuthContext or add AuthApi helper—document choice in PR.
```

### DB-01 — Core models

Add **decision line** (avoids late migration pain):

```text
Default: extend via Profile (OneToOne to django.contrib.auth.models.User) unless the team
commits in this issue to a custom AUTH_USER_MODEL before any production data.
```

### API-01 / API-02 / API-03 / FE-03 / FE-04

Add to each:

```text
All new routes: include in docs/api-endpoints.md and @extend_schema on views;
path prefix /api/v1/ (include via config.api_v1_urls).
```

### DOC-01 — Swagger

Clarify:

```text
Global entry: /api/docs/ and /api/schema/ (not under /v1). Per-endpoint docs follow each view.
```

---

## Labels / board (optional, reduces confusion)

- Add label `api-v1` on any issue that defines HTTP routes.
- **Close** an issue only if **code + tests + api-endpoints.md** (when applicable) match the description, or the description was updated to match the code.

---

## What you cannot fix only in Issues

- **PM-01** (board permissions, milestones): settings live on GitHub; link this file from the **team wiki** or **README** once DOC-02 exists.
