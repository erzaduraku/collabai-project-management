# CollabAI – Project Management

> **Distributed Systems Project** · Spring 2026  
> Team: Erza · Edonita · Leona · Engji · Fatlinda

---

## 📋 Project Overview

CollabAI is a multi-tenant, AI-assisted project management platform built with:

- **Backend** – Django REST Framework (DRF), JWT auth, Celery, Redis, PostgreSQL
- **Frontend** – React with Context API
- **AI** – OpenAI integration for task summarization and priority suggestions
- **Infrastructure** – GitHub Actions CI/CD, Docker

---

## 🚀 Quick Start – Import All Issues

All 26 project tasks are stored in [`tasks.csv`](./tasks.csv).  
Run the **Import Issues** workflow to create them as GitHub Issues with proper labels, milestones, and assignees.

### Step 1 – Trigger the import workflow

1. Go to **Actions → Import Issues from CSV**
2. Click **Run workflow**
3. (Optional) Enter GitHub usernames for each team member:
   - **Edonita** username
   - **Leona** username
   - **Engji** username
   - **Fatlinda** username
4. Click **Run workflow**

The workflow will:
- ✅ Create all **labels** (backend, frontend, auth, db, api, etc.)
- ✅ Create **3 milestones** (Sprint 1 → Sprint 2 → Sprint 3)
- ✅ Create all **26 issues** with titles, descriptions, acceptance criteria
- ✅ Assign issues to team members
- ✅ Link issues to milestones and apply priority labels
- ✅ Skip duplicates if re-run

### Step 2 – Create the Project Board

1. Go to **Actions → Create GitHub Project Board**
2. Click **Run workflow**
3. *(Requires a PAT with `project` scope stored as secret `PROJECT_TOKEN`)*

---

## 📁 Repository Structure

```
collabai-project-management/
├── tasks.csv                          # All 26 tasks (source of truth)
├── .github/
│   ├── workflows/
│   │   ├── import-issues.yml          # Workflow: imports tasks.csv → GitHub Issues
│   │   └── create-project.yml         # Workflow: creates Projects v2 board
│   └── scripts/
│       ├── import_issues.py           # Python script: labels + milestones + issues
│       └── create_project.py          # Python script: Projects v2 board via GraphQL
└── README.md
```

---

## 🗂️ Sprint Plan

| Sprint | Dates | Focus |
|--------|-------|-------|
| **Sprint 1** | Apr 27 – May 9 | Setup, Auth, Core Models, Basic Frontend |
| **Sprint 2** | May 10 – May 14 | CRUD APIs, Dashboard, Task Board, CI, Cache |
| **Sprint 3** | May 15 – May 20 | AI, Search, Docs, Final Integration |

---

## 📌 Tasks at a Glance

### Sprint 1 (9 tasks)

| ID | Task | Assignee | Points | Priority |
|----|------|----------|--------|----------|
| PM-01 | GitHub Project Setup | Erza | 3 | 🔴 High |
| ARCH-01 | DRF + OOP Guidelines | Edonita | 5 | 🔴 High |
| AUTH-01 | Register API | Erza | 5 | 🔴 High |
| DB-01 | Core Models | Leona | 6 | 🔴 High |
| AUTH-02 | Login + JWT | Engji | 4 | 🔴 High |
| MIDDLEWARE-01 | Logging + Auth | Erza | 5 | 🟡 Medium |
| FE-01 | React + Context Setup | Edonita | 5 | 🔴 High |
| FE-02 | Auth UI | Edonita | 5 | 🔴 High |
| DB-02 | 20+ Models + Migration | Leona | 7 | 🔴 High |

### Sprint 2 (10 tasks)

| ID | Task | Assignee | Points | Priority |
|----|------|----------|--------|----------|
| MT-01 | Multi-Tenancy Data Isolation | Leona | 5 | 🔴 High |
| API-01 | CRUD APIs | Engji | 6 | 🔴 High |
| CACHE-01 | Redis | Fatlinda | 5 | 🟡 Medium |
| TEST-01 | Unit Tests | Leona | 5 | 🟡 Medium |
| FE-03 | Dashboard | Engji | 5 | 🟡 Medium |
| FE-04 | Task Board | Fatlinda | 5 | 🔴 High |
| CI-01 | GitHub Actions | Fatlinda | 5 | 🟡 Medium |
| API-02 | Extra Endpoints | Engji | 5 | 🔴 High |
| FE-05 | Role UI | Edonita | 3 | 🟡 Medium |
| TEST-02 | E2E | Fatlinda | 6 | 🟡 Medium |

### Sprint 3 (7 tasks)

| ID | Task | Assignee | Points | Priority |
|----|------|----------|--------|----------|
| API-03 | Search + Filtering | Engji | 5 | 🟡 Medium |
| AI-01 | OpenAI + Celery | Erza | 7 | 🔴 High |
| ASYNC-01 | Email + Jobs | Erza | 6 | 🟡 Medium |
| FE-06 | AI UI | Edonita | 5 | 🟡 Medium |
| DOC-01 | Swagger | Leona | 4 | 🟡 Medium |
| DOC-02 | README | Fatlinda | 5 | 🟢 Low |
| FINAL-01 | Final Integration | All | 8 | 🔴 High |

**Total story points: 131**

---

## 🏷️ Labels

| Label | Color | Description |
|-------|-------|-------------|
| `backend` | Blue | Backend / Django / DRF work |
| `frontend` | Yellow | Frontend / React work |
| `auth` | Red-Orange | Authentication & Authorization |
| `db` | Blue | Database models & migrations |
| `api` | Dark Blue | REST API endpoints |
| `testing` | Light Blue | Tests (unit, integration, e2e) |
| `ci` | Light Blue | CI/CD pipeline |
| `docs` | Yellow | Documentation |
| `ai` | Dark Red | AI / OpenAI integration |
| `pm` | Teal | Project management |
| `middleware` | Blue | Middleware |
| `tenant` | Blue | Multi-tenancy |
| `redis` | Red | Redis / Caching |
| `search` | Dark Blue | Search & filtering |
| `celery` | Dark Red | Celery async tasks |
| `async` | Dark Red | Async background jobs |
| `e2e` | Light Blue | End-to-end testing |
| `swagger` | Yellow | Swagger / OpenAPI docs |
| `final` | Teal | Final integration |
| `priority:high` | Red | High priority |
| `priority:medium` | Yellow | Medium priority |
| `priority:low` | Green | Low priority |

---

## 👥 Team

| Name | Role | GitHub |
|------|------|--------|
| Erza | PM + Backend Lead | [@erzaduraku](https://github.com/erzaduraku) |
| Edonita | Architecture + Frontend | TBD |
| Leona | Database + Backend | TBD |
| Engji | API + Backend | TBD |
| Fatlinda | Frontend + CI/CD | TBD |

---

## 📜 Course Requirements Coverage

| # | Requirement | Task(s) |
|---|-------------|---------|
| 1 | Distributed architecture | ARCH-01, MT-01 |
| 2 | HTTP/HTTPS communication | AUTH-01, AUTH-02, API-01, API-02 |
| 3 | 20+ REST endpoints | API-01, API-02, API-03 |
| 4 | RESTful API Framework (DRF) | ARCH-01, API-01 |
| 5 | OOP Programming | ARCH-01, DB-01 |
| 6 | Multi-tenancy | MT-01 |
| 7 | ORM & Database | DB-01, DB-02 |
| 8 | Authentication & Authorization | AUTH-01, AUTH-02, MIDDLEWARE-01 |
| 9 | Role-based access control | FE-05, AUTH-02 |
| 10 | Caching (Redis) | CACHE-01 |
| 11 | Background Jobs (Celery) | AI-01, ASYNC-01 |
| 12 | AI Integration (OpenAI) | AI-01, FE-06 |
| 13 | Email notifications | ASYNC-01 |
| 14 | CI/CD Pipeline | CI-01 |
| 15 | Unit Testing | TEST-01 |
| 16 | E2E Testing | TEST-02 |
| 17 | API Documentation (Swagger) | DOC-01 |
| 18 | Frontend (React) | FE-01 through FE-06 |
| 19 | Project Documentation | DOC-02 |
| 20 | Search & Filtering | API-03 |
